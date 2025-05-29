from pymclevel import TAG_Byte, TAG_Int
import math

displayName = "Xisuma's Cart Filter"

inputs = (("Check:",("Above","Below")),("Block Separation Height:",(16,-2147483648,2147483647)),)
	
def perform(level, box, options):
	check = options["Check:"]
	blockheight = options["Block Separation Height:"]

	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.Entities:
			x = e["Pos"][0].value
			y = e["Pos"][1].value
			z = e["Pos"][2].value
		
			if (x,y,z) in box:
				if "Minecart" in e["id"].value:
					fx = int(math.floor(x))
					fy = int(math.floor(y)+1)
					fz = int(math.floor(z))
					for ly in xrange(fy,box.maxy if check == "Above" else box.miny, 1  if check == "Above" else -1):
						block = level.blockAt(fx,ly,fz)
						if block != 0:
							data = level.blockDataAt(fx,ly,fz)
							e["CustomDisplayTile"] = TAG_Byte(1)
							e["DisplayTile"] = TAG_Int(block)
							e["DisplayData"] = TAG_Int(data)
							e["DisplayOffset"] = TAG_Int((ly - (fy-1))*blockheight)
							level.setBlockAt(fx, ly, fz, 0)
							level.setBlockDataAt(fx, ly, fz, 0)
							chunk.dirty = True
							break
					else:
						print "Unable to find block for cart at:",x,y,z