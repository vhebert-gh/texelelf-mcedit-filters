from pymclevel import TAG_Byte, TAG_Short
from pymclevel import TileEntity

displayName = "Mirror Sign Posts"

North = ( 0,  1,  2,  3, 13, 14, 15 )
South = { 5,  6,  7,  8,  9, 10, 11 }
East =  ( 1,  2,  3,  4,  5,  6,  7 )
West =  ( 9, 10, 11, 12, 13, 14, 15 )

NorthToSouth = { 13:11, 14:10, 15:9, 0:8, 1:7, 2:6, 3:5 }
SouthToNorth = { 11:13, 10:14, 9:15, 8:0, 7:1, 6:2, 5:3 }
EastToWest   = {  1:15, 2:14, 3:13, 4:12, 5:11, 6:10, 7:9 }
WestToEast   = {  15:1, 14:2, 13:3, 12:4, 11:5, 10:6, 9:7 }


inputs = (
	("Mirror Along:",("X Axis (North-South)","Z Axis (East-West)")),
	)
	
def perform(level, box, options):
	mirrorz = True if options["Mirror Along:"] == "Z Axis (East-West)" else False
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			for y in xrange(box.miny, box.maxy):
				if level.blockAt(x,y,z) == 63:
					rot = level.blockDataAt(x, y, z)
					if mirrorz:
						if rot in East:
							level.setBlockDataAt(x, y, z, EastToWest[rot])
						elif rot in West:
							level.setBlockDataAt(x, y, z, WestToEast[rot])
					else:
						if rot in North:
							level.setBlockDataAt(x, y, z, NorthToSouth[rot])
						elif rot in South:
							level.setBlockDataAt(x, y, z, SouthToNorth[rot])
					