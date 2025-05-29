from pymclevel import TAG_Byte, TAG_Int, TAG_Compound, TAG_String
import inspect
from pymclevel import MCSchematic

MAXCLONESIZE = 32768

displayName = "To Clone Command"

inputs = (	("Operation:",("Set Source Volume","Set Destination","Output current source volume information")),
			("Split Source Volume into multiple clone commands",False),
			("Sub-Volume Dimensions (XxYxZ):",("string","value=1x1x1")),
			("Clone air blocks",True),
			("Prevent creation of clone operations greater than "+str(MAXCLONESIZE)+" blocks:",True),
			)

try:
	srcBox
except NameError:
	srcBox = None
	
def CommandBlock(x,y,z,command):
	cmd = TAG_Compound()
	cmd["x"] = TAG_Int(x)
	cmd["y"] = TAG_Int(y)
	cmd["z"] = TAG_Int(z)
	cmd["id"] = TAG_String("Control")
	cmd["Command"] = TAG_String(command)
	cmd["TrackOutput"] = TAG_Byte(0)
	return cmd

def perform(level, box, options):
	editor = inspect.stack()[1][0].f_locals.get('self', None).editor

	global srcBox
	op = options["Operation:"]
	idiotproof = options["Prevent creation of clone operations greater than "+str(MAXCLONESIZE)+" blocks:"]
	mask = "" if options["Clone air blocks"] else "masked"
	if op == "Set Source Volume":
		srcBox = box
		sx, sy, sz = srcBox.size
		if (sx*sy*sz) > MAXCLONESIZE:
			raise Exception("Source Volume set at x:"+str(box.minx)+", y:"+str(box.miny)+", z:"+str(box.minz)+" to x:"+str(box.maxx)+", y:"+str(box.maxy)+", z:"+str(box.maxz)+"\nWARNING: The source selection has more than "+str(MAXCLONESIZE)+" blocks in it; either select a smaller volume, or use sub-volumes.")
		else:
			raise Exception("Source Volume set at x:"+str(box.minx)+", y:"+str(box.miny)+", z:"+str(box.minz)+" to x:"+str(box.maxx)+", y:"+str(box.maxy)+", z:"+str(box.maxz))
	elif op == "Output current source volume information":
		bx,by,bz = box.size
		raise Exception("Source Volume is at x:"+str(box.minx)+", y:"+str(box.miny)+", z:"+str(box.minz)+" to x:"+str(box.maxx)+", y:"+str(box.maxy)+", z:"+str(box.maxz)+"\nThe dimensions are: "+str(bx)+"x"+str(by)+"x"+str(bz))

	if srcBox.size != box.size:
		raise Exception("The Source and Destination Volumes aren't the same size!  They must be the same dimensions in order to continue.")

	split = options["Split Source Volume into multiple clone commands"]
	if split:
		sx, sy, sz = options["Sub-Volume Dimensions (XxYxZ):"].split("x")
		sx = int(sx)
		sy = int(sy)
		sz = int(sz)
		if idiotproof:
			if (sx*sy*sz) > MAXCLONESIZE:
				raise Exception("Unable to use the desired sub-volume dimensions; there are more than "+str(MAXCLONESIZE)+" blocks in the volume.")

		bx,by,bz = box.size
		if (bx % sx) or (by % sy) or (bz % sz):
			raise Exception("The source volume is not a multiple of the provided sub-volume dimensions. The sub-volume dimensions must fit evenly inside of the source volume.")
		width = int(bx/sx)
		height = int(by/sy)
		length = int(bz/sz)
	else:
		sx, sy, sz = box.size
		if idiotproof:
			if (sx*sy*sz) > MAXCLONESIZE:
				raise Exception("Unable to use the desired volume dimensions; there are more than "+str(MAXCLONESIZE)+" blocks in the volume.")
		width = height = length = 1

	srcx,srcy,srcz = srcBox.origin
	destx,desty,destz = box.origin
	
	schematic = MCSchematic((width, height, length), mats=level.materials)
	for y in xrange(height):
		for z in xrange(length):
			for x in xrange(width):
				x1 = srcx+(x*sx)
				y1 = srcy+(y*sy)
				z1 = srcz+(z*sz)
				x2 = (x1+sx)-1
				y2 = (y1+sy)-1
				z2 = (z1+sz)-1
				dx = destx+(x*sx)
				dy = desty+(y*sy)
				dz = destz+(z*sz)
				command = "clone {} {} {} {} {} {} {} {} {} {}".format(x1,y1,z1,x2,y2,z2,dx,dy,dz,mask)
				schematic.setBlockAt(x, y, z, 137)
				schematic.setBlockDataAt(x, y, z, 0)
				schematic.TileEntities.append(CommandBlock(x,y,z,command))

	editor.addCopiedSchematic(schematic)
	raise Exception("Schematic successfully added to clipboard.")
