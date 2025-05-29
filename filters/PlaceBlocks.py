from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float, TAG_Long, TAG_Byte_Array, TAG_Int_Array
from pymclevel.materials import alphaMaterials
import math
import inspect
from pymclevel import MCSchematic
from copy import deepcopy

displayName = "Place Blocks"

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

inputs = [
	(("Operation:",("Place Blocks in Selection","Place Below Blocks")),
	("Blocks to Place:", alphaMaterials.Stone),
	("Place Operation:",("replace","keep","destroy")),
	("The following two options are only valid for \"in selection\" operations.","label"),
	("Ignore Air Blocks:",True),
	("Include TileEntity NBT data:",True),
	("Use \"minecraft:\" prefix for Block ID",False),
	("General","title"),),
	
	(("Block Filtering:", ("None","Only the Below","Except the Below")),
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

def perform(level, box, options):
	editor = inspect.stack()[1][0].f_locals.get('self', None).editor
	op = options["Operation:"]
	swap = options["Blocks to Place:"]
	method = options["Place Operation:"]
	tents = options["Include TileEntity NBT data:"]
	useprefix = options["Use \"minecraft:\" prefix for Block ID"]
	
	filter = options["Block Filtering:"]
	ignoreair = options["Ignore Air Blocks:"]
	ignore = options["Ignore Damage Value"]

	FilterBlock = []
	
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

	sx,sy,sz = box.size
	width = sx + math.ceil(float(sx)/float(15))
	height = sy * 2
	length = sz + (math.ceil(float(sz)%float(3)))
	schematic = MCSchematic((width, height, length), mats=level.materials)

	yctr = 0
	for y in xrange(box.miny, box.maxy):
		zctr = 0
		for z in xrange(box.minz, box.maxz):
			xctr = 0
			blockcounter = 0
			xadd = 0
			for x in xrange(box.minx, box.maxx):
				place = True
				block = level.blockAt(x, y, z)
				if block == 0 and ignoreair:
					place = False
				data = level.blockDataAt(x, y, z)
				if filter != "None":
					if filter == "Only the Below" and ((block,(data if not ignore else 0)) not in FilterBlock):
						place = False
					elif filter == "Except the Below" and ((block,(data if not ignore else 0)) in FilterBlock):
						 place = False
				if place:
					if tents and op == "Place Blocks in Selection":
						e = level.tileEntityAt(x,y,z)
						if e == None:
							mdata = ""
						else:
							tileent = deepcopy(e)
							if "x" in tileent:
								del tileent["x"]
							if "y" in tileent:
								del tileent["y"]
							if "z" in tileent:
								del tileent["z"]
							if "id" in tileent:
								del tileent["id"]
							mdata = "{"+NBT2Command(tileent)+"}"
					else:
						mdata = ""

					if op == "Place Blocks in Selection":
						tileid = block
						blockdata = data
					else:
						tileid = swap.ID
						blockdata = swap.blockData
					if tileid in block_map:
						if useprefix:
							tileid = block_map[tileid]
						else:
							tileid = block_map[tileid][10:]

					command = TAG_String(unicode("setblock {} {} {} {} {} {} {}".format(unicode(x), unicode(y), unicode(z), unicode(tileid), unicode(blockdata), unicode(method), unicode(mdata)).decode("unicode-escape")))

					newcommand = TAG_Compound()
					newcommand["id"] = TAG_String("Control")
					newcommand["x"] = TAG_Int(xctr+xadd)
					newcommand["y"] = TAG_Int(yctr*2)
					newcommand["z"] = TAG_Int(zctr)
					newcommand["TrackOutput"] = TAG_Byte(0)
					newcommand["Command"] = command

					schematic.setBlockAt(xctr+xadd, yctr*2, zctr, 137)
					schematic.setBlockDataAt(xctr+xadd, yctr*2, zctr, 0)
					schematic.TileEntities.append(newcommand)

				blockcounter += 1
				if not (zctr % 3):
					schematic.setBlockAt(xctr+xadd, (yctr*2), zctr+1, 1)
					schematic.setBlockDataAt(xctr+xadd, (yctr*2), zctr+1, 0)
					schematic.setBlockAt(xctr+xadd, (yctr*2)+1, zctr+1, 55)
					schematic.setBlockDataAt(xctr+xadd, (yctr*2)+1, zctr+1, 0)
					if blockcounter == 15:
						schematic.setBlockAt(xctr+xadd+1, (yctr*2), zctr+1, 1)
						schematic.setBlockDataAt(xctr+xadd+1, (yctr*2), zctr+1, 0)
						schematic.setBlockAt(xctr+xadd+1, (yctr*2)+1, zctr+2, 89)
						schematic.setBlockDataAt(xctr+xadd+1, (yctr*2)+1, zctr+2, 0)
						schematic.setBlockAt(xctr+xadd+1, (yctr*2)+1, zctr+1, 93)
						schematic.setBlockDataAt(xctr+xadd+1, (yctr*2)+1, zctr+1, 1)
				
				if blockcounter >= 15:
					blockcounter = 0
					xadd += 1
				xctr += 1
			zctr += 1
		yctr += 1

	editor.addCopiedSchematic(schematic)
	raise Exception("Schematic successfully added to clipboard.")
