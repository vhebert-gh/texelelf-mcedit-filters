from pymclevel import TAG_Byte

displayName = "Fix Lag"

def perform(level, box, options):
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:
				if e["id"].value == "Control":
					e["TrackOutput"] = TAG_Byte(0)
					if "LastOutput" in e:
						del e["LastOutput"]
					chunk.dirty = True
