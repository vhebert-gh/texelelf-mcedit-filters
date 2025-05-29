from pymclevel import TAG_Byte, TAG_Short
from pymclevel.materials import alphaMaterials


displayName = "Block Liner"

inputs = (
	("Lining Block:", alphaMaterials.Air),
	("Line...","label"),
	("Shape:",(	"Directional",
				"Inside Sphere",
				"Outside Sphere",
				"Inside Vertical Cyllinder",
				"Outside Vertical Cyllinder",
				"Inside Horizontal X Cyllinder",
				"Outside Horizontal X Cyllinder",
				"Inside Horizontal Z Cyllinder",
				"Outside Horizontal Z Cyllinder")),
	("+X-wards",False),
	("-X-wards",False),
	("Upwards",False),
	("Downwards",False),
	("+Z-wards",False),
	("-Z-wards",False),
	)
	
def perform(level, box, options):
	burn = options["Lining Block:"]
	shape = options["Shape:"]
	up = options["Upwards"]
	down = options["Downwards"]
	px = options["+X-wards"]
	nx = options["-X-wards"]
	pz = options["+Z-wards"]
	nz = options["-Z-wards"]
	burnblocks = []
	width, height, length = box.size
		
	for x in xrange(box.minx, box.maxx):
		rx = x - box.minx
		for z in xrange(box.minz, box.maxz):
			rz = z - box.minz
			for y in xrange(box.miny, box.maxy):
				ry = y - box.miny
				if level.blockAt(x,y,z) != 0:
					if shape == "Inside Sphere":
						if rx <= (width / 2):
							px = True
							nx = False
						else:
							px = False
							nx = True
						if rz <= (length / 2):
							pz = True
							nz = False
						else:
							pz = False
							nz = True
						if ry <= (height / 2):
							up = True
							down = False
						else:
							up = False
							down = True
					elif shape == "Outside Sphere":
						if rx >= (width / 2):
							px = True
							nx = False
						else:
							px = False
							nx = True
						if rz >= (length / 2):
							pz = True
							nz = False
						else:
							pz = False
							nz = True
						if ry >= (height / 2):
							up = True
							down = False
						else:
							up = False
							down = True
					elif shape == "Inside Vertical Cyllinder":
						if rx <= (width / 2):
							px = True
							nx = False
						else:
							px = False
							nx = True
						if rz <= (length / 2):
							pz = True
							nz = False
						else:
							pz = False
							nz = True
						up = False
						down = False
					elif shape == "Outside Vertical Cyllinder":
						if rx >= (width / 2):
							px = True
							nx = False
						else:
							px = False
							nx = True
						if rz >= (length / 2):
							pz = True
							nz = False
						else:
							pz = False
							nz = True
						up = False
						down = False
					if shape == "Inside Horizontal X Cyllinder":
						if rz <= (length / 2):
							pz = True
							nz = False
						else:
							pz = False
							nz = True
						if ry <= (height / 2):
							up = True
							down = False
						else:
							up = False
							down = True
						px = False
						nx = False
					elif shape == "Outside Horizontal X Cyllinder":
						if rz >= (length / 2):
							pz = True
							nz = False
						else:
							pz = False
							nz = True
						if ry >= (height / 2):
							up = True
							down = False
						else:
							up = False
							down = True
						px = False
						nx = False
					if shape == "Inside Horizontal Z Cyllinder":
						if rx <= (width / 2):
							px = True
							nx = False
						else:
							px = False
							nx = True
						if ry <= (height / 2):
							up = True
							down = False
						else:
							up = False
							down = True
						pz = False
						nz = False
					elif shape == "Outside Horizontal Z Cyllinder":
						if rx >= (width / 2):
							px = True
							nx = False
						else:
							px = False
							nx = True
						if ry >= (height / 2):
							up = True
							down = False
						else:
							up = False
							down = True
						pz = False
						nz = False

					if nx:
						if level.blockAt(x-1,y,z) == 0:
							burnblocks.append((x-1,y,z))
					if px:
						if level.blockAt(x+1,y,z) == 0:
							burnblocks.append((x+1,y,z))
					if down:
						if level.blockAt(x,y-1,z) == 0:
							burnblocks.append((x,y-1,z))
					if up:
						if level.blockAt(x,y+1,z) == 0:
							burnblocks.append((x,y+1,z))
					if nz:
						if level.blockAt(x,y,z-1) == 0:
							burnblocks.append((x,y,z-1))
					if pz:
						if level.blockAt(x,y,z+1) == 0:
							burnblocks.append((x,y,z+1))

	for x,y,z in burnblocks:
		level.setBlockAt(x, y, z, burn.ID)
		level.setBlockDataAt(x, y, z, burn.blockData)
