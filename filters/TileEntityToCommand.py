from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float, TAG_Long, TAG_Byte_Array, TAG_Int_Array
from copy import deepcopy

displayName = "TileEntity to Command Block"
inputs = (
	("Command Block Type:",("Command Blocks","Minecart Command Blocks")),
	("Coordinates are Relative to Command Block",True),
	("X Spawn Position",0.0),
	("Y Spawn Position",0.0),
	("Z Spawn Position",0.0),
	("Overwrite Spawner Coordinates",False),
	)

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
	blocktype = options["Command Block Type:"]
	relative = options["Coordinates are Relative to Command Block"]
	overwrite = options["Overwrite Spawner Coordinates"]
	posx = options["X Spawn Position"]
	posy = options["Y Spawn Position"]
	posz = options["Z Spawn Position"]
	entsToAdd = []
	entsToDelete = []
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:
				if e["id"].value == "MobSpawner":
					if "SpawnData" not in e:
						sx = "~"
						sy = "~"
						sz = "~"
						spawndata = ""
					else:
						spawn = deepcopy(e["SpawnData"])
						if "Pos" not in spawn:
							sx = "~"
							sy = "~"
							sz = "~"
							spawndata = "{"+NBT2Command(spawn)+"}"
						else:
							sx = "%.2f"%spawn["Pos"][0].value
							sy = "%.2f"%spawn["Pos"][1].value
							sz = "%.2f"%spawn["Pos"][2].value
							del spawn["Pos"]
							spawndata = "{"+NBT2Command(spawn)+"}"
					type = e["EntityId"].value
					if overwrite:
						if relative:
							sx = "~" + (str(posx) if posx != 0.0 else "")
							sy = "~" + (str(posy) if posy != 0.0 else "")
							sz = "~" + (str(posz) if posz != 0.0 else "")
						else:
							sx = str(posx)
							sy = str(posy)
							sz = str(posz)
				else:
					block = level.blockAt(x, y, z)
					if block in block_map:
						block = block_map[block]
					data = level.blockDataAt(x, y, z)
					type = "setblock"
					spawn = deepcopy(e)
					if "x" in spawn:
						del spawn["x"]
					if "y" in spawn:
						del spawn["y"]
					if "z" in spawn:
						del spawn["z"]
					spawndata = "{"+NBT2Command(spawn)+"}"
					if relative:
						sx = "~" + (str(posx) if posx != 0.0 else "")
						sy = "~" + (str(posy) if posy != 0.0 else "")
						sz = "~" + (str(posz) if posz != 0.0 else "")
					else:
						sx = str(posx)
						sy = str(posy)
						sz = str(posz)
				if type == "setblock":
					command = TAG_String(unicode("setblock {} {} {} {} {} {} {}".format(unicode(sx), unicode(sy), unicode(sz), unicode(block), unicode(data), unicode("replace"), unicode(spawndata)).decode("unicode-escape")))
				else:
					command = TAG_String(unicode("summon {} {} {} {} {}".format(unicode(type), unicode(sx), unicode(sy), unicode(sz), unicode(spawndata)).decode("unicode-escape")))
				if blocktype == "Command Blocks":
					newcommand = TAG_Compound()
					newcommand["id"] = TAG_String("Control")
					newcommand["x"] = TAG_Int(x)
					newcommand["y"] = TAG_Int(y)
					newcommand["z"] = TAG_Int(z)
					newcommand["Command"] = command
					level.setBlockAt(x, y, z, 137)
					level.setBlockDataAt(x, y, z, 0)
				else:
					newcommand = TAG_Compound()
					newcommand["id"] = TAG_String("MinecartCommandBlock")
					newcommand["Fire"] = TAG_Short(-1)
					newcommand["OnGround"] = TAG_Byte(0)
					newcommand["FallDistance"] = TAG_Float(0.0)
					newcommand["Rotation"] = TAG_List([TAG_Float(0.0),TAG_Float(0.0)])
					newcommand["Motion"] = TAG_List([TAG_Double(0.0),TAG_Double(0.0),TAG_Double(0.0)])
					newcommand["Command"] = command
					newcommand["CustomName"] = TAG_String("@")
					newcommand["Pos"] = TAG_List([TAG_Double(float(x)+0.5),TAG_Double(float(y)+0.5),TAG_Double(float(z)+0.5)])
					level.setBlockAt(x, y, z, 0)
					level.setBlockDataAt(x, y, z, 0)
				entsToAdd.append((chunk,newcommand))
				entsToDelete.append((chunk, e))

	for (chunk, entity) in entsToAdd:
		if blocktype == "Command Blocks":
			chunk.TileEntities.append(entity)
		else:
			chunk.Entities.append(entity)
		chunk.dirty = True
				
	for (chunk, entity) in entsToDelete:
		chunk.TileEntities.remove(entity)
		chunk.dirty = True


