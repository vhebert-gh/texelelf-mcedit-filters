from pymclevel import TAG_List
from copy import deepcopy

displayName = "Repair Chunk Entities"

def perform(level, box, options):
	entities = []
	for cx, cz in level.allChunks:
		chunk = level.getChunk(cx, cz)
		entities += deepcopy(chunk.Entities)
		del chunk.Entities
		chunk.Entities = TAG_List()
		chunk.dirty = True

	for e in entities:
		if "Pos" not in e:
			continue
		cx = int(e["Pos"][0].value)>>4
		cz = int(e["Pos"][2].value)>>4
		chunk = level.getChunk(cx, cz)
		chunk.Entities.append(deepcopy(e))
		chunk.dirty = True
