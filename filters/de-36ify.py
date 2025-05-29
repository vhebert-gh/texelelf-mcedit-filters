from pymclevel import TAG_Compound
from pymclevel import TAG_String
from pymclevel import TAG_Int
from pymclevel import TAG_Float
from pymclevel import TAG_Byte
from pymclevel import TileEntity
from pymclevel import BoundingBox
from pymclevel.materials import alphaMaterials

displayName = "De-36ify"

inputs = (
	("X width",10),
	("Y height",10),
	("Z length",10),
	("Use block held by Piston (ignores below)",False),
	("Replace 36 with: ",alphaMaterials.Air)
	)

def perform(level, box, options):
	sizex = options["X width"]
	sizey = options["Y height"]
	sizez = options["Z length"]
	useblock = options["Use block held by Piston (ignores below)"]
	replace = options["Replace 36 with: "]
	ents = []
	newbox = BoundingBox((box.minx+sizex if sizex <= 0 else box.minx, box.miny+sizey if sizey <= 0 else box.miny, box.minz+sizez if sizez <= 0 else box.minz),(abs(sizex), abs(sizey), abs(sizez)))

	print box
	print newbox
	print newbox.minx, newbox
	print box.minx, box.maxx, box.miny, box.maxy, box.minz, box.maxz
	print box.minx+sizex if sizex <= 0 else box.minx, box.miny+sizey if sizey <= 0 else box.miny, box.minz+sizez if sizez <= 0 else box.minz, box.maxz if sizez <= 0 else box.maxz+sizez
	
	for y in xrange(newbox.miny, newbox.maxy, 1):
		for x in xrange(newbox.minx, newbox.maxx, 1):
			for z in xrange(newbox.minz, newbox.maxz, 1):
				if level.blockAt(x, y, z) == 36:
					e = level.tileEntityAt(x, y, z)
					if e != None:
						ents.append(e)
					if useblock and e != None:
						level.setBlockAt(x, y, z, e["blockId"].value)
						level.setBlockDataAt(x, y, z, e["blockData"].value)
					else:
						level.setBlockAt(x, y, z, replace.ID)
						level.setBlockDataAt(x, y, z, replace.blockData)

	for (chunk, slices, point) in level.getChunkSlices(newbox):
		(cx,cz) = chunk.chunkPosition
		cposx = cx * 16
		cposz = cz * 16
		for en in ents:
			x = en["x"].value
			z = en["z"].value
			if x >= cposx and x < cposx+16 and z >= cposz and z < cposz+16:
				print x, z
				chunk.TileEntities.remove(en)
		chunk.dirty = True
