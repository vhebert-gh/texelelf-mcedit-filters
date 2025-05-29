from pymclevel import TAG_Byte
from pymclevel import TAG_String
from pymclevel import Entity

displayName = "Tomutwit's Make Giant Filter"

inputs = (
	("Persistent",True),
	)

def perform(level, box, options):

	persist = options["Persistent"]

	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.Entities:
			x = e["Pos"][0].value
			y = e["Pos"][1].value
			z = e["Pos"][2].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if "Health" in e:
					e["id"] = TAG_String("Giant")
					e["PersistenceRequired"] = TAG_Byte(persist)
					chunk.dirty = True