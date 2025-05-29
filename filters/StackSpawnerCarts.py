from pymclevel import Entity, TAG_Double

displayName = "Stack MinecartSpawner Entities"

inputs = (
	("X Stack Location:",0.5),
	("Y Stack Location:",0.5),
	("Z Stack Location:",0.5),
	)

def perform(level, box, options):

	xstack = options["X Stack Location:"]
	ystack = options["Y Stack Location:"]
	zstack = options["Z Stack Location:"]
	entitylist = []
	delentities = []

	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.Entities:
			if "Pos" not in e:
				continue
			x = e["Pos"][0].value
			y = e["Pos"][1].value
			z = e["Pos"][2].value
			if (x,y,z) in box:
				if e["id"].value == "MinecartSpawner":
					e["Pos"][0] = TAG_Double(xstack)
					e["Pos"][1] = TAG_Double(ystack)
					e["Pos"][2] = TAG_Double(zstack)
					entitylist.append(e)
					delentities.append((chunk,e))
					chunk.dirty = True
	for (c, e) in delentities:
		c.Entities.remove(e)
	poschunk = level.getChunk(int(xstack/16),int(zstack/16))
	for e in entitylist:
		poschunk.Entities.append(e)
