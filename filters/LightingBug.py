from pymclevel import TAG_Int_Array
from pymclevel.level import extractHeights

displayName = "Lighting Bug Filter"

inputs = (
	("Operation:",("Create Lighting Bug","Fix Lighting Bug")),

	)
def perform(level, box, options):
	op = options["Operation:"]

	for (chunk, slices, point) in level.getChunkSlices(box):
		miny = box.miny
		(cx,cz) = chunk.chunkPosition
		cposx = cx * 16
		cposz = cz * 16
		if op == "Fix Lighting Bug":
			del chunk.root_tag["Level"]["HeightMap"]
			newheightmap = extractHeights(chunk.Blocks)
			chunk.root_tag["Level"]["HeightMap"] = TAG_Int_Array(newheightmap)
			chunk.dirty = True
			chunk.needsLighting = True
		else:
			hm = chunk.root_tag["Level"]["HeightMap"].value.view(dtype="uint16").flatten()
			for y in xrange(box.miny,box.maxy,1):
				for z in xrange(max(cposz, box.minz),min(cposz+16, box.maxz),1):
					for x in xrange(max(cposx, box.minx),min(cposx+16, box.maxx),1):
						chx = x-cposx
						chz = z-cposz
						hm[(chz<<4)+chx] = miny
						chunk.SkyLight[chx,chz,y] = 0xF
						chunk.BlockLight[chx,chz,y] = 0xF
			chunk.root_tag["Level"]["HeightMap"] = TAG_Int_Array(hm)
			chunk.dirty = True
			chunk.needsLighting = False
						