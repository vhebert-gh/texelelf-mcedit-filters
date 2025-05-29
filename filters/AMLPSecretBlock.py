from pymclevel import TAG_Compound
from pymclevel import TAG_String
from pymclevel import TAG_Int
from pymclevel import TAG_Float
from pymclevel import TAG_Byte
from pymclevel import TileEntity
from pymclevel.materials import alphaMaterials

displayName = "AMLP's Secret Block Filter"

inputs = [
	(("Delay Until Start",10.0),
	("Delay between each block",0.2),
	("Delay between rows",0.6),
	("Delay between layers",0.6),
	("Complete one row at a time",False),
	("Complete one layer at a time",False),
	("East-West Fill Progression:",("Eastwards (+X to -X)","Westwards (-X to +X)")),
	("North-South Fill Progression:",("Northwards (+Z to -Z)","Southwards (-Z to +Z)")),
	("Vertical Fill Progression:",("Upwards (-Y to +Y)","Downwards (+Y to -Y)")),
	("Ignore air blocks",True),
	("General Settings","title"),),
	
	(("Operation:", ("Ignore","Use Only Below","Do Not Use Below")),
	("Ignore Damage Value",False),
	("Filter Block 1", alphaMaterials.Air),
	("Filter Block 2", alphaMaterials.Air),
	("Filter Block 3", alphaMaterials.Air),
	("Filter Block 4", alphaMaterials.Air),
	("Filter Block 5", alphaMaterials.Air),
	("Filter Block 6", alphaMaterials.Air),
	("Filter Block 7", alphaMaterials.Air),
	("Filter Block 8", alphaMaterials.Air),
	("Filter Block 9", alphaMaterials.Air),
	("Filter Block 10", alphaMaterials.Air),
	("Filter Block Options","title"),),
	]

def perform(level, box, options):
	ignoreair = options["Ignore air blocks"]
	start = float(options["Delay Until Start"] * -1.0)
	delay = options["Delay between each block"]

	rowdelay = options["Delay between rows"]
	layerdelay = options["Delay between layers"]
	onerow = options["Complete one row at a time"]
	onelayer = options["Complete one layer at a time"]
	
	eastwest = options["East-West Fill Progression:"]
	northsouth = options["North-South Fill Progression:"]
	updown = options["Vertical Fill Progression:"]
	
	east = True if eastwest == "Eastwards (+X to -X)" else False
	north = True if northsouth == "Northwards (+Z to -Z)" else False
	up = True if updown == "Upwards (-Y to +Y)" else False

	entities = []
	FilterBlock = []
	
	op = options["Operation:"]
	ignore = options["Ignore Damage Value"]
	
	FilterBlock.append((options["Filter Block 1"].ID,(options["Filter Block 1"].blockData if not ignore else 0)))
	if options["Filter Block 2"].ID != 0:
		FilterBlock.append((options["Filter Block 2"].ID,(options["Filter Block 2"].blockData if not ignore else 0)))
	if options["Filter Block 3"].ID != 0:
		FilterBlock.append((options["Filter Block 3"].ID,(options["Filter Block 3"].blockData if not ignore else 0)))
	if options["Filter Block 4"].ID != 0:
		FilterBlock.append((options["Filter Block 4"].ID,(options["Filter Block 4"].blockData if not ignore else 0)))
	if options["Filter Block 5"].ID != 0:
		FilterBlock.append((options["Filter Block 5"].ID,(options["Filter Block 5"].blockData if not ignore else 0)))
	if options["Filter Block 6"].ID != 0:
		FilterBlock.append((options["Filter Block 6"].ID,(options["Filter Block 6"].blockData if not ignore else 0)))
	if options["Filter Block 7"].ID != 0:
		FilterBlock.append((options["Filter Block 7"].ID,(options["Filter Block 7"].blockData if not ignore else 0)))
	if options["Filter Block 8"].ID != 0:
		FilterBlock.append((options["Filter Block 8"].ID,(options["Filter Block 8"].blockData if not ignore else 0)))
	if options["Filter Block 9"].ID != 0:
		FilterBlock.append((options["Filter Block 9"].ID,(options["Filter Block 9"].blockData if not ignore else 0)))	
	if options["Filter Block 10"].ID != 0:
		FilterBlock.append((options["Filter Block 10"].ID,(options["Filter Block 10"].blockData if not ignore else 0)))
	current = start
	yc = 0
	xc = 0
	oldcurrent = current
	
	for y in xrange(box.miny if up else box.maxy-1, box.maxy if up else box.miny-1, 1 if up else -1):
		if not onelayer:
			current = start + ((yc*layerdelay)*-1.0)
			yc += 1
		oldcurrent = current
		xc = 0
		for x in xrange(box.maxx-1 if east else box.minx, box.minx-1 if east else box.maxx, -1 if east else 1):
			if not onerow:
				current = oldcurrent + ((xc*rowdelay)*-1.0)
				xc += 1
			for z in xrange(box.maxz-1 if north else box.minz, box.minz-1 if north else box.maxz, -1 if north else 1):
				block = level.blockAt(x, y, z)
				data = level.blockDataAt(x,y,z)
				if block == 0:
					if ignoreair:
						continue
				elif block == 36:
					continue
				if op == "Use Only Below" and ((block,(data if not ignore else 0)) not in FilterBlock):
					continue
				elif op == "Do Not Use Below" and ((block,(data if not ignore else 0)) in FilterBlock):
					continue
				current -= delay
				e = TileEntity.Create("Piston")
				e["blockId"] = TAG_Int(block)
				e["blockData"] = TAG_Int(data)
				e["progress"] = TAG_Float(current)
				TileEntity.setpos(e, (x, y, z))
				entities.append(e)
				level.setBlockAt(x, y, z, 36)

	for (chunk, slices, point) in level.getChunkSlices(box):
		(cx,cz) = chunk.chunkPosition
		cposx = cx << 4
		cposz = cz << 4
		chunk.dirty = True
		for e in entities:
			x = e["x"].value
			z = e["z"].value
			if x >= cposx and x < cposx+16 and z >= cposz and z < cposz+16:
				chunk.TileEntities.append(e)
				chunk.dirty = True
	