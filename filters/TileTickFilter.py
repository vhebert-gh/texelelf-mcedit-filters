from pymclevel import TAG_Compound, TAG_Int, TAG_Short, TAG_Byte, TAG_Byte_Array, TAG_String, TAG_List
from pymclevel.materials import alphaMaterials
from numpy import zeros
from random import randint

displayName = "Tile Tick Filter"

inputs = [
	(("Update Operation:",("Progressive","At Once","Random","Delete TileTicks")),
	("East-West Progression:",("Eastwards (+X to -X)","Westwards (-X to +X)")),
	("North-South Progression:",("Northwards (+Z to -Z)","Southwards (-Z to +Z)")),
	("Vertical Progression:",("Upwards (-Y to +Y)","Downwards (+Y to -Y)")),
	("Complete one row at a time",False),
	("Complete one layer at a time",False),
	("Ticks Until Start",(200,-2147483648,2147483647)),
	("Ticks between each block",(2,-2147483648,2147483647)),
	("Ticks between rows",(10,-2147483648,2147483647)),
	("Ticks between layers",(10,-2147483648,2147483647)),
	("Minimum Random Tick Range",(50,-2147483648,2147483647)),
	("Maximum Random Tick Range",(100,-2147483648,2147483647)),
	("Tile Tick Options","title")),
	
	(("Operation:", ("Ignore","Use Only Below","Do Not Use Below")),
	("Filter Block 1", alphaMaterials.Air),
	("Filter Block 2", alphaMaterials.Air),
	("Filter Block 3", alphaMaterials.Air),
	("Filter Block 4", alphaMaterials.Air),
	("Filter Block 5", alphaMaterials.Air),
	("Block Filtering Options","title"))
]

def perform(level, box, options):
	upop = options["Update Operation:"]
	start = options["Ticks Until Start"]
	delay = options["Ticks between each block"]

	rowdelay = options["Ticks between rows"]
	layerdelay = options["Ticks between layers"]
	onerow = options["Complete one row at a time"]
	onelayer = options["Complete one layer at a time"]
	
	eastwest = options["East-West Progression:"]
	northsouth = options["North-South Progression:"]
	updown = options["Vertical Progression:"]
	minrand = options["Minimum Random Tick Range"]
	maxrand = options["Maximum Random Tick Range"]
	
	east = True if eastwest == "Eastwards (+X to -X)" else False
	north = True if northsouth == "Northwards (+Z to -Z)" else False
	up = True if updown == "Upwards (-Y to +Y)" else False

	FilterBlock = []
	op = options["Operation:"]
	FilterBlock.append(options["Filter Block 1"].ID)
	if options["Filter Block 2"].ID != 0:
		FilterBlock.append(options["Filter Block 2"].ID)
	if options["Filter Block 3"].ID != 0:
		FilterBlock.append(options["Filter Block 3"].ID)
	if options["Filter Block 4"].ID != 0:
		FilterBlock.append(options["Filter Block 4"].ID)
	if options["Filter Block 5"].ID != 0:
		FilterBlock.append(options["Filter Block 5"].ID)
	

	if upop == "Delete TileTicks":
		for (chunk, slices, point) in level.getChunkSlices(box):
			if "TileTicks" in chunk.root_tag["Level"]:
				for ind in xrange(len(chunk.root_tag["Level"]["TileTicks"])-1,-1,-1):
					tickx = chunk.root_tag["Level"]["TileTicks"][ind]["x"].value
					ticky = chunk.root_tag["Level"]["TileTicks"][ind]["y"].value
					tickz = chunk.root_tag["Level"]["TileTicks"][ind]["z"].value
					if (tickx,ticky,tickz) in box:
						del chunk.root_tag["Level"]["TileTicks"][ind]
						chunk.dirty = True
		return
				
	ticks = []
	current = start
	yc = 0
	xc = 0
	oldcurrent = current
	for y in xrange(box.miny if up else box.maxy-1, box.maxy if up else box.miny-1, 1 if up else -1):
		if not onelayer:
			current = start + (yc*layerdelay)
			yc += 1
		oldcurrent = current
		xc = 0
		for x in xrange(box.maxx-1 if east else box.minx, box.minx-1 if east else box.maxx, -1 if east else 1):
			if not onerow:
				current = oldcurrent + (xc*rowdelay)
				xc += 1
			for z in xrange(box.maxz-1 if north else box.minz, box.minz-1 if north else box.maxz, -1 if north else 1):
				block = level.blockAt(x, y, z)
				if block == 0:
					continue
				if op == "Use Only Below" and block not in FilterBlock:
					continue
				elif op == "Do Not Use Below" and block in FilterBlock:
					continue
				current += delay
				e = TAG_Compound()
				e["i"] = TAG_Int(block)
				if upop == "Progressive":
					e["t"] = TAG_Int(current)
				elif upop == "At Once":
					e["t"] = TAG_Int(start)
				elif upop == "Random":
					minval = min(minrand,maxrand)+start
					maxval = max(minrand,maxrand)+start
					e["t"] = TAG_Int(randint(minval,maxval))
				e["x"] = TAG_Int(x)
				e["y"] = TAG_Int(y)
				e["z"] = TAG_Int(z)
				ticks.append(e)
				del e

	for (chunk, slices, point) in level.getChunkSlices(box):
		(cx,cz) = chunk.chunkPosition
		cposx = cx << 4
		cposz = cz << 4
		ticklist = [tick for tick in ticks if (tick["x"].value >= cposx and tick["x"].value < cposx+16 and tick["z"].value >= cposz and tick["z"].value < cposz+16)]
		for e in ticklist:
			if "TileTicks" not in chunk.root_tag["Level"]:
				chunk.root_tag["Level"]["TileTicks"] = TAG_List()
			chunk.root_tag["Level"]["TileTicks"].append(e)
			chunk.dirty = True
				
