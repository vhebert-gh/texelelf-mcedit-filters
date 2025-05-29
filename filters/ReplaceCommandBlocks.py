displayName = "Replace Command Blocks"

inputs = (
	("Replace if:",("Matching","Not Matching")),
	("Match:",("string","value=None")),
	("Replace with:", "blocktype"),
	)

def perform(level, box, options):
	match = options["Match:"]
	if match == "None":
		raise Exception("No valid matching string provided!")
		return
	replace = options["Replace if:"]
	replaceblock = options["Replace with:"]

	TileentsToDelete = []
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			
			if (x,y,z) in box:
				if e["id"].value == "Control":
					if "Command" in e:
						if match in e["Command"].value:
							if replace == "Matching":
								TileentsToDelete.append((chunk,e))
								level.setBlockAt(x,y,z,replaceblock.ID)
								level.setBlockDataAt(x,y,z,replaceblock.blockData)
						else:
							if replace == "Not Matching":
								TileentsToDelete.append((chunk,e))
								level.setBlockAt(x,y,z,replaceblock.ID)
								level.setBlockDataAt(x,y,z,replaceblock.blockData)
	for chunk, e in TileentsToDelete:
		chunk.TileEntities.remove(e)
		chunk.dirty = True