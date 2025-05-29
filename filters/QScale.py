import inspect
from pymclevel import TAG_Int
from pymclevel import MCSchematic
import math
from copy import deepcopy

displayName = "Q-Magnet's Scaler"

inputs = (
	("Scale X by:",1.0),
	("Scale Y by:",1.0),
	("Scale Z by:",1.0),
	)


def perform(level, box, options):
	global editor
	try:
		editor
	except:
		editor = inspect.stack()[1][0].f_locals.get('self', None).editor

	xscale = options["Scale X by:"]
	yscale = options["Scale Y by:"]
	zscale = options["Scale Z by:"]

	width,height,length = box.size
	ox, oy, oz = box.origin
	swidth = int(math.floor(width*xscale))
	sheight = int(math.floor(height*yscale))
	slength = int(math.floor(length*zscale))
	schematic = MCSchematic((swidth, sheight, slength), mats=level.materials)
	for x in xrange(swidth):
		for y in xrange(sheight):
			for z in xrange(slength):
				px = int(math.floor(x / xscale))+ox
				py = int(math.floor(y / yscale))+oy
				pz = int(math.floor(z / zscale))+oz

				block = level.blockAt(px, py, pz)
				data = level.blockDataAt(px, py, pz)
				
				schematic.setBlockAt(x, y, z, block)
				schematic.setBlockDataAt(x, y, z, data)
				
				tileent = level.tileEntityAt(px, py, pz)
				if tileent:
					newtileent = deepcopy(tileent)
					newtileent["x"] = TAG_Int(x)
					newtileent["y"] = TAG_Int(y)
					newtileent["z"] = TAG_Int(z)
					schematic.TileEntities.append(newtileent)
					
	editor.addCopiedSchematic(schematic)
	raise Exception("Schematic successfully added to clipboard.")
