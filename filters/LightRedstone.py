from random import randrange, shuffle
from pymclevel.materials import alphaMaterials

displayName = "Light Up Redstone"
	
repeaters = ( 93, 94 )
comparators = ( 149, 150 )
torches = ( 75, 76 )
	
inputs = (
	("Light up Repeaters",True),
	("Light up Comparators",True),
	("Light up Torches",True),
	)

def perform(level, box, options):
	repeat = options["Light up Repeaters"]
	compare = options["Light up Comparators"]
	torch = options["Light up Torches"]
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			for y in xrange(box.miny, box.maxy):
				block = level.blockAt(x,y,z)
				if (repeat and block in repeaters) or (compare and block in comparators) or (torch and block in torches):
					if level.blockAt(x,y+1,z) == 0:
						level.setBlockAt(x, y+1, z, 89)
						level.setBlockDataAt(x, y+1, z, 0)
					elif level.blockAt(x+1,y,z) == 0:
						level.setBlockAt(x+1, y, z, 89)
						level.setBlockDataAt(x+1, y, z, 0)
					elif level.blockAt(x-1,y,z) == 0:
						level.setBlockAt(x-1, y, z, 89)
						level.setBlockDataAt(x-1, y, z, 0)
					elif level.blockAt(x,y,z+1) == 0:
						level.setBlockAt(x, y, z+1, 89)
						level.setBlockDataAt(x, y, z+1, 0)
					elif level.blockAt(x,y,z-1) == 0:
						level.setBlockAt(x, y, z-1, 89)
						level.setBlockDataAt(x, y, z-1, 0)
						
