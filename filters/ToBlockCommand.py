import inspect
from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float, TAG_Long, TAG_Byte_Array, TAG_Int_Array
from pymclevel import MCSchematic
from pymclevel.materials import alphaMaterials
import math
from copy import deepcopy

MAXCLONESIZE = 32768

displayName = "To Block Command"

inputs = [	(("Command type to create:",("clone","fill","testforblocks","setblock","testforblock","blockdata","summon")),
			("Operation:",("Set Source Volume","Set Destination","Output current source volume information")),
			("Split Source Volume into multiple clone\\fill\\testforblocks commands",False),
			("Sub-Volume Dimensions (XxYxZ):",("string","value=32x32x32")),
			("Clone\\testforblocks with air blocks",True),
			("Mirror clone across X axis",False),
			("Mirror clone across Y axis",False),
			("Mirror clone across Z axis",False),
			("Fill block:", alphaMaterials.Air),
			("Fill method:",("None","replace","destroy","keep","hollow","outline")),
			("Block to replace:", alphaMaterials.Air),
			("Prevent creation of clone\\fill\\testforblocks operations greater than "+str(MAXCLONESIZE)+" blocks:",True),
			("General Options","title"),),

			(("Use \"Set or Test\" below with setblock\\testforblock instead of the blocks in the selection:",False),
			("Set or Test for block:", alphaMaterials.Air),
			("Ignore air blocks with setblock\\testforblock\\blockdata:",True),
			("Setblock method:",("replace","keep","destroy")),
			("Do not create blockdata commands for blocks with no NBT data:",True),
			("Time value for summoned FallingSand:",(1,-128,127)),
			("Set\\Testfor\\Blockdata","title"),),

			(("Block filtering is only valid for setblock, testforblock, and blockdata "
			  "commands.  These options are ignored for clone, fill, and testforblocks commands.","label"),
			("Block Filtering:", ("None","Only the Below","Except the Below")),
			("Ignore Damage Value",False),
			("Filter Block 1", alphaMaterials.Air),
			("Filter Block 2", alphaMaterials.Air),
			("Filter Block 3", alphaMaterials.Air),
			("Filter Block 4", alphaMaterials.Air),
			("Filter Block 5", alphaMaterials.Air),
			("Filter Block 6", alphaMaterials.Air),
			("Filter Block 7", alphaMaterials.Air),
			("Filter Block 8", alphaMaterials.Air),
			("Block Filtering","title"),),
		]

block_map = {
	0:"minecraft:air",1:"minecraft:stone",2:"minecraft:grass",3:"minecraft:dirt",4:"minecraft:cobblestone",5:"minecraft:planks",6:"minecraft:sapling",
	7:"minecraft:bedrock",8:"minecraft:flowing_water",9:"minecraft:water",10:"minecraft:flowing_lava",11:"minecraft:lava",12:"minecraft:sand",13:"minecraft:gravel",
	14:"minecraft:gold_ore",15:"minecraft:iron_ore",16:"minecraft:coal_ore",17:"minecraft:log",18:"minecraft:leaves",19:"minecraft:sponge",20:"minecraft:glass",
	21:"minecraft:lapis_ore",22:"minecraft:lapis_block",23:"minecraft:dispenser",24:"minecraft:sandstone",25:"minecraft:noteblock",26:"minecraft:bed",
	27:"minecraft:golden_rail",28:"minecraft:detector_rail",29:"minecraft:sticky_piston",30:"minecraft:web",31:"minecraft:tallgrass",32:"minecraft:deadbush",
	33:"minecraft:piston",34:"minecraft:piston_head",35:"minecraft:wool",36:"minecraft:piston_extension",37:"minecraft:yellow_flower",38:"minecraft:red_flower",
	39:"minecraft:brown_mushroom",40:"minecraft:red_mushroom",41:"minecraft:gold_block",42:"minecraft:iron_block",43:"minecraft:double_stone_slab",
	44:"minecraft:stone_slab",45:"minecraft:brick_block",46:"minecraft:tnt",47:"minecraft:bookshelf",48:"minecraft:mossy_cobblestone",49:"minecraft:obsidian",
	50:"minecraft:torch",51:"minecraft:fire",52:"minecraft:mob_spawner",53:"minecraft:oak_stairs",54:"minecraft:chest",55:"minecraft:redstone_wire",
	56:"minecraft:diamond_ore",57:"minecraft:diamond_block",58:"minecraft:crafting_table",59:"minecraft:wheat",60:"minecraft:farmland",61:"minecraft:furnace",
	62:"minecraft:lit_furnace",63:"minecraft:standing_sign",64:"minecraft:wooden_door",65:"minecraft:ladder",66:"minecraft:rail",67:"minecraft:stone_stairs",
	68:"minecraft:wall_sign",69:"minecraft:lever",70:"minecraft:stone_pressure_plate",71:"minecraft:iron_door",72:"minecraft:wooden_pressure_plate",
	73:"minecraft:redstone_ore",74:"minecraft:lit_redstone_ore",75:"minecraft:unlit_redstone_torch",76:"minecraft:redstone_torch",77:"minecraft:stone_button",
	78:"minecraft:snow_layer",79:"minecraft:ice",80:"minecraft:snow",81:"minecraft:cactus",82:"minecraft:clay",83:"minecraft:reeds",84:"minecraft:jukebox",
	85:"minecraft:fence",86:"minecraft:pumpkin",87:"minecraft:netherrack",88:"minecraft:soul_sand",89:"minecraft:glowstone",90:"minecraft:portal",
	91:"minecraft:lit_pumpkin",92:"minecraft:cake",93:"minecraft:unpowered_repeater",94:"minecraft:powered_repeater",
	95:"minecraft:stained_glass",96:"minecraft:trapdoor",97:"minecraft:monster_egg",98:"minecraft:stonebrick",
	99:"minecraft:brown_mushroom_block",100:"minecraft:red_mushroom_block",101:"minecraft:iron_bars",102:"minecraft:glass_pane",103:"minecraft:melon_block",
	104:"minecraft:pumpkin_stem",105:"minecraft:melon_stem",106:"minecraft:vine",107:"minecraft:fence_gate",108:"minecraft:brick_stairs",109:"minecraft:stone_brick_stairs",
	110:"minecraft:mycelium",111:"minecraft:waterlily",112:"minecraft:nether_brick",113:"minecraft:nether_brick_fence",114:"minecraft:nether_brick_stairs",
	115:"minecraft:nether_wart",116:"minecraft:enchanting_table",117:"minecraft:brewing_stand",118:"minecraft:cauldron",119:"minecraft:end_portal",
	120:"minecraft:end_portal_frame",121:"minecraft:end_stone",122:"minecraft:dragon_egg",123:"minecraft:redstone_lamp",124:"minecraft:lit_redstone_lamp",
	125:"minecraft:double_wooden_slab",126:"minecraft:wooden_slab",127:"minecraft:cocoa",128:"minecraft:sandstone_stairs",129:"minecraft:emerald_ore",
	130:"minecraft:ender_chest",131:"minecraft:tripwire_hook",132:"minecraft:tripwire",133:"minecraft:emerald_block",134:"minecraft:spruce_stairs",
	135:"minecraft:birch_stairs",136:"minecraft:jungle_stairs",137:"minecraft:command_block",138:"minecraft:beacon",139:"minecraft:cobblestone_wall",
	140:"minecraft:flower_pot",141:"minecraft:carrots",142:"minecraft:potatoes",143:"minecraft:wooden_button",144:"minecraft:skull",145:"minecraft:anvil",
	146:"minecraft:trapped_chest",147:"minecraft:light_weighted_pressure_plate",148:"minecraft:heavy_weighted_pressure_plate",149:"minecraft:unpowered_comparator",
	150:"minecraft:powered_comparator",151:"minecraft:daylight_detector",152:"minecraft:redstone_block",153:"minecraft:quartz_ore",154:"minecraft:hopper",
	155:"minecraft:quartz_block",156:"minecraft:quartz_stairs",157:"minecraft:activator_rail",158:"minecraft:dropper",159:"minecraft:stained_hardened_clay",
	160:"minecraft:stained_glass_pane",162:"minecraft:log2",163:"minecraft:acacia_stairs",164:"minecraft:dark_oak_stairs",165:"minecraft:slime",166:"minecraft:barrier",
	167:"minecraft:iron_trapdoor",168:"minecraft:prismarine",169:"minecraft:sea_lantern",
	170:"minecraft:hay_block",171:"minecraft:carpet",172:"minecraft:hardened_clay",173:"minecraft:coal_block",174:"minecraft:packed_ice",175:"minecraft:double_plant"
}

try:
	srcBox
except NameError:
	srcBox = None

def NBT2Command(nbtData):
	command = ""
	if type(nbtData) is TAG_List:
		list = True
	else:
		list = False

	for tag in range(0,len(nbtData)) if list else nbtData.keys():
		if type(nbtData[tag]) is TAG_Compound:
			if not list:
				if tag != "":
					command += tag+":"
			command += "{"
			command += NBT2Command(nbtData[tag])
			command += "}"
		elif type(nbtData[tag]) is TAG_List:
			if not list:
				if tag != "":
					command += tag+":"
			command += "["
			command += NBT2Command(nbtData[tag])
			command += "]"
		else:
			if not list:
				if tag != "":
					command += tag+":"
			if type(nbtData[tag]) is TAG_String:
				command += "\""
				command += str.replace(nbtData[tag].value.encode("unicode-escape"), r'"',r'\\"')
				command += "\""
			else:
				if type(nbtData[tag]) == TAG_Byte_Array:
					command += "["+",".join(["%sb" % num for num in nbtData[tag].value.astype("str")])+"]"
				elif type(nbtData[tag]) == TAG_Int_Array:
					command += "["+",".join(nbtData[tag].value.astype("str"))+"]"
				else:
					command += nbtData[tag].value.encode("unicode-escape") if isinstance(nbtData[tag].value, unicode) else str(nbtData[tag].value)
					if type(nbtData[tag]) is TAG_Byte:
						command += "b"
					elif type(nbtData[tag]) is TAG_Short:
						command += "s"
					elif type(nbtData[tag]) is TAG_Long:
						command += "l"
					elif type(nbtData[tag]) is TAG_Float:
						command += "f"
					elif type(nbtData[tag]) is TAG_Double:
						command += "d"			
		command += ","
	else:
		if command != "":
			if command[-1] == ",":
				command = command[:-1]
	return command

def CommandBlock(x,y,z,command):
	cmd = TAG_Compound()
	cmd["x"] = TAG_Int(x)
	cmd["y"] = TAG_Int(y)
	cmd["z"] = TAG_Int(z)
	cmd["id"] = TAG_String("Control")
	cmd["Command"] = TAG_String(command)
	cmd["TrackOutput"] = TAG_Byte(0)
	return cmd

def perform(level, box, options):
	editor = inspect.stack()[1][0].f_locals.get('self', None).editor

	global srcBox
	type = options["Command type to create:"]
	op = options["Operation:"]
	fillblock = options["Fill block:"]
	if fillblock.ID in block_map:
		fillID = block_map[fillblock.ID]
	else:
		fillID = fillblock.ID
	doreplace = options["Fill method:"]
	replaceblock = options["Block to replace:"]
	if replaceblock.ID in block_map:
		replaceID = block_map[replaceblock.ID]
	else:
		replaceID = replaceblock.ID
	idiotproof = options["Prevent creation of clone\\fill\\testforblocks operations greater than "+str(MAXCLONESIZE)+" blocks:"]
	mask = "" if options["Clone\\testforblocks with air blocks"] else "masked"
	split = options["Split Source Volume into multiple clone\\fill\\testforblocks commands"]

	axisx = options["Mirror clone across X axis"]
	axisy = options["Mirror clone across Y axis"]
	axisz = options["Mirror clone across Z axis"]
	mirror = axisx or axisy or axisz

	usefill = options["Use \"Set or Test\" below with setblock\\testforblock instead of the blocks in the selection:"]
	setblock = options["Set or Test for block:"]
	if type == "summon" and usefill:
		if setblock.ID == 0:
			raise Exception("Unable to summon FallingSand air blocks.")
	ignoreair = options["Ignore air blocks with setblock\\testforblock\\blockdata:"]
	method = options["Setblock method:"]
	enforcenbt = options["Do not create blockdata commands for blocks with no NBT data:"]
	time = options["Time value for summoned FallingSand:"]

	FilterBlock = []
	filter = options["Block Filtering:"]
	ignore = options["Ignore Damage Value"]
	
	if options["Filter Block 1"].ID != 0:
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

	if type in ("setblock","testforblock","blockdata","summon"):
		width,height,length = box.size
		schematic = MCSchematic((width, height, length), mats=level.materials)
		for y in xrange(box.miny, box.maxy):
			for z in xrange(box.minz, box.maxz):
				for x in xrange(box.minx, box.maxx):
					block = level.blockAt(x, y, z)
					if block == 0:
						if type == "summon":
							if not usefill:
								continue
						elif ignoreair:
							continue
					data = level.blockDataAt(x, y, z)
					if filter != "None":
						if filter == "Only the Below" and ((block,(data if not ignore else 0)) not in FilterBlock):
							continue
						elif filter == "Except the Below" and ((block,(data if not ignore else 0)) in FilterBlock):
							continue

					if usefill:
						tileid = setblock.ID
						blockdata = setblock.blockData
					else:
						tileid = block
						blockdata = data
					if tileid in block_map:
						tileid = block_map[tileid]

					if usefill and type != "blockdata":
						mdata = ""
						if type == "summon":
							newcomp = TAG_Compound()
							newcomp["Block"] = TAG_String(tileid)
							newcomp["Data"] = TAG_Byte(blockdata)
							newcomp["Time"] = TAG_Byte(time)
							mdata = "{"+NBT2Command(newcomp)+"}"
					else:
						e = level.tileEntityAt(x,y,z)
						if e == None:
							if enforcenbt and type == "blockdata":
								continue
							mdata = ""
							if type == "summon":
								newcomp = TAG_Compound()
								newcomp["Block"] = TAG_String(tileid)
								newcomp["Data"] = TAG_Byte(blockdata)
								newcomp["Time"] = TAG_Byte(time)
								mdata = "{"+NBT2Command(newcomp)+"}"
						else:
							tileent = deepcopy(e)
							del tileent["x"]
							del tileent["y"]
							del tileent["z"]
							del tileent["id"]
							if type == "summon":
								newcomp = TAG_Compound()
								newcomp["Block"] = TAG_String(tileid)
								newcomp["Data"] = TAG_Byte(blockdata)
								newcomp["Time"] = TAG_Byte(time)
								newcomp["TileEntityData"] = tileent
								mdata = "{"+NBT2Command(newcomp)+"}"
							else:
								mdata = "{"+NBT2Command(tileent)+"}"


					if type == "setblock":
						command = unicode("setblock {} {} {} {} {} {} {}".format(unicode(x), unicode(y), unicode(z), unicode(tileid), unicode(blockdata), unicode(method), unicode(mdata)).decode("unicode-escape"))
					elif type == "blockdata":
						command = unicode("blockdata {} {} {} {}".format(unicode(x), unicode(y), unicode(z), unicode(mdata)).decode("unicode-escape"))
					elif type == "summon":
						command = unicode("summon FallingSand {} {} {} {}".format(unicode(x), unicode(y), unicode(z), unicode(mdata)).decode("unicode-escape"))
					else:
						command = unicode("testforblock {} {} {} {} {} {}".format(unicode(x), unicode(y), unicode(z), unicode(tileid), unicode(blockdata), unicode(mdata)).decode("unicode-escape"))
					if command[-1] == " ":
						command = command[:-1]
					schematic.setBlockAt(x-box.minx, y-box.miny, z-box.minz, 137)
					schematic.setBlockDataAt(x-box.minx, y-box.miny, z-box.minz, 0)
					schematic.TileEntities.append(CommandBlock(x-box.minx,y-box.miny,z-box.minz,command))

	elif type == "fill":
		if split:
			sx, sy, sz = options["Sub-Volume Dimensions (XxYxZ):"].split("x")
			sx = int(sx)
			sy = int(sy)
			sz = int(sz)
			if idiotproof:
				if (sx*sy*sz) > MAXCLONESIZE:
					raise Exception("Unable to use the desired sub-volume dimensions; there are more than "+str(MAXCLONESIZE)+" blocks in the volume.")
			bx, by, bz = box.size
			width = int(math.ceil(float(bx)/float(sx)))
			height = int(math.ceil(float(by)/float(sy)))
			length = int(math.ceil(float(bz)/float(sz)))
		else:
			sx, sy, sz = box.size
			if idiotproof:
				if (sx*sy*sz) > MAXCLONESIZE:
					raise Exception("Unable to use the desired volume dimensions; there are more than "+str(MAXCLONESIZE)+" blocks in the volume.")
			width = height = length = 1

		swx,swy,swz = box.size
		srcx,srcy,srcz = box.origin
		schematic = MCSchematic((width, height, length), mats=level.materials)
		for y in xrange(height):
			for z in xrange(length):
				for x in xrange(width):
					x1 = srcx+(x*sx)
					y1 = srcy+(y*sy)
					z1 = srcz+(z*sz)

					if (x*sx)+sx > swx:
						zx = swx % sx
					else:
						zx = sx
					if (y*sy)+sy > swy:
						zy = swy % sy
					else:
						zy = sy
					if (z*sz)+sz > swz:
						zz = swz % sz
					else:
						zz = sz
					x2 = (x1+zx)-1
					y2 = (y1+zy)-1
					z2 = (z1+zz)-1
					if doreplace == "None":
						command = "fill {} {} {} {} {} {} {} {}".format(x1,y1,z1,x2,y2,z2,fillID,fillblock.blockData)
					elif doreplace == "replace":
						command = "fill {} {} {} {} {} {} {} {} replace {} {}".format(x1,y1,z1,x2,y2,z2,fillID,fillblock.blockData,replaceID,replaceblock.blockData)
					else:
						command = "fill {} {} {} {} {} {} {} {} {}".format(x1,y1,z1,x2,y2,z2,fillID,fillblock.blockData,doreplace)
					schematic.setBlockAt(x, y, z, 137)
					schematic.setBlockDataAt(x, y, z, 0)
					schematic.TileEntities.append(CommandBlock(x,y,z,command))

	elif type in ("clone","testforblocks"):
		if op == "Set Source Volume":
			srcBox = box
			sx, sy, sz = srcBox.size
			if (sx*sy*sz) > MAXCLONESIZE:
				raise Exception("Source Volume set at x:"+str(box.minx)+", y:"+str(box.miny)+", z:"+str(box.minz)+" to x:"+str(box.maxx)+", y:"+str(box.maxy)+", z:"+str(box.maxz)+"\nWARNING: The source selection has more than "+str(MAXCLONESIZE)+" blocks in it; either select a smaller volume, or use sub-volumes.")
			else:
				raise Exception("Source Volume set at x:"+str(box.minx)+", y:"+str(box.miny)+", z:"+str(box.minz)+" to x:"+str(box.maxx)+", y:"+str(box.maxy)+", z:"+str(box.maxz))
		elif op == "Output current source volume information":
			bx,by,bz = box.size
			raise Exception("Source Volume is at x:"+str(box.minx)+", y:"+str(box.miny)+", z:"+str(box.minz)+" to x:"+str(box.maxx)+", y:"+str(box.maxy)+", z:"+str(box.maxz)+"\nThe dimensions are: "+str(bx)+"x"+str(by)+"x"+str(bz))

		if srcBox.size != box.size:
			sx,sy,sz = srcBox.size
			dx,dy,dz = box.size
			raise Exception("The Source and Destination Volumes aren't the same size!  They must be the same dimensions in order to continue.\n"
							"The Source dimensions are: "+str(sx)+"x"+str(sy)+"x"+str(sz)+"\n"
							"The Destination dimensions are: "+str(dx)+"x"+str(dy)+"x"+str(dz))

		if split:
			sx, sy, sz = options["Sub-Volume Dimensions (XxYxZ):"].split("x")
			sx = int(sx)
			sy = int(sy)
			sz = int(sz)
			if idiotproof:
				if (sx*sy*sz) > MAXCLONESIZE:
					raise Exception("Unable to use the desired sub-volume dimensions; there are more than "+str(MAXCLONESIZE)+" blocks in the volume.")
			bx, by, bz = box.size
			width = int(math.ceil(float(bx)/float(sx)))
			height = int(math.ceil(float(by)/float(sy)))
			length = int(math.ceil(float(bz)/float(sz)))
		else:
			sx, sy, sz = box.size
			if idiotproof:
				if (sx*sy*sz) > MAXCLONESIZE:
					raise Exception("Unable to use the desired volume dimensions; there are more than "+str(MAXCLONESIZE)+" blocks in the volume.")
			width = height = length = 1

		srcx,srcy,srcz = srcBox.origin
		destx,desty,destz = box.origin
		swx,swy,swz = srcBox.size

		if mirror:
			if axisx:
				width *= sx
				sx = 1
			if axisy:
				height *= sy
				sy = 1
			if axisz:
				length *= sz
				sz = 1
		
		schematic = MCSchematic((width, height, length), mats=level.materials)
		for y in xrange(height):
			for z in xrange(length):
				for x in xrange(width):
					x1 = srcx+(x*sx)
					y1 = srcy+(y*sy)
					z1 = srcz+(z*sz)

					if (x*sx)+sx > swx:
						zx = swx % sx
					else:
						zx = sx
					if (y*sy)+sy > swy:
						zy = swy % sy
					else:
						zy = sy
					if (z*sz)+sz > swz:
						zz = swz % sz
					else:
						zz = sz

					x2 = (x1+zx)-1
					y2 = (y1+zy)-1
					z2 = (z1+zz)-1

					dx = destx+(x*sx)
					dy = desty+(y*sy)
					dz = destz+(z*sz)
					if mirror:
						if axisx:
							dx = box.maxx-(x*sx)-1
						if axisy:
							dy = box.maxy-(y*sy)-1
						if axisz:
							dz = box.maxz-(z*sz)-1
					
					command = "{} {} {} {} {} {} {} {} {} {} {}".format(type,x1,y1,z1,x2,y2,z2,dx,dy,dz,mask)
					if command[-1] == " ":
						command = command[:-1]
					schematic.setBlockAt(x, y, z, 137)
					schematic.setBlockDataAt(x, y, z, 0)
					schematic.TileEntities.append(CommandBlock(x,y,z,command))
					
	editor.addCopiedSchematic(schematic)
	raise Exception("Schematic successfully added to clipboard.")
