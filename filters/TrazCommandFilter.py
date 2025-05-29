from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float, TAG_Long
from pymclevel import BoundingBox
from copy import deepcopy
import math
import re

displayName = "TrazLander's Command Spawn Filter"

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
	160:"minecraft:stained_glass_pane",161:"minecraft:leaves2",162:"minecraft:log2",163:"minecraft:acacia_stairs",164:"minecraft:dark_oak_stairs",165:"minecraft:slime",
	166:"minecraft:barrier",167:"minecraft:iron_trapdoor",168:"minecraft:prismarine",169:"minecraft:sea_lantern",
	170:"minecraft:hay_block",171:"minecraft:carpet",172:"minecraft:hardened_clay",173:"minecraft:coal_block",174:"minecraft:packed_ice",175:"minecraft:double_plant"
}

inputs = [
	(("Use full block name for setblock commands", False),
	("Remove Signs Upon Completion",True),
	("Remove Blocks\\Entities Upon Completion (midway signs only)",True),
	("Find\\Remove Variable:",("string","value=NONE")),
	("Replace\\Add Variable:",("string","value=NONE")),
	("Operation:",(	"Create Command Blocks",
					"Find\\Replace Sign Text",
					"Empty All Sign Text",
					"Populate Sign TileEntities",
					"Convert Signs: Wall -> Standing",
					"Convert Signs: Standing -> Wall")),
	("Defaults","title")),

	(("%s:<id>\t Source"
	"\n%d:<id>\t Destination"
	"\n_______________________________________"
	"\n%m:<id> Optional: Minecart Command Block location\n\t\t-Pair with '%m:<id>' \n\t\t on any %s signs"
	"\nid:<id>  Optional: Unique, case-insensitive ID \n\t\t-Pair with src/dest/midway"
	"\n_______________________________________"
	"\n\nent\t  Add to %s signs:\n\t\t-Spawns projectile/item/mob entity"
	"\nent fw\t Add to %s signs:\n\t\t-Spawns FireworksRocketEntity","label"),
	("Base Params","title"),),
	
	(("(d)x: (d)y: (d)z:\tAdds value to Coordinates"
	"\n(d)vx: (d)vy: (d)vz:   Adds value to Velocity"
	"\n(d)yw: (d)ph:\t\tSets Yaw & Pitch Rotation"
	"\n\n(d)t:\t Time FallingSand has existed"
	"\n(d)i\t  Invulnerable entity"
	"\n(d)dr\tDropItem: destroyed FallingSand drops item"
	"\n(d)a:\tAge: despawn time"
	"\n(d)fr:\t Fire: entity is burning"
	"\n(d)h\tHurtEntities: FallingSand inflicts damage\n\t\tto entities it intersects"
	"\n(d)hm:\tFallHurtMax: max damage inflicted"
	"\n(d)fd:\t  FallDistance: distance entity has fallen"
	"\n(d)ha:\t FallHurtAmount: multiply by FallDistance"
	"\n(d)bt:\t BurnTime (Furnaces)"
	"\n(d)fs:\t  Fuse (PrimedTNT)"
	"\n(d)er:\t ExplosionRadius (PrimedTNT)"
	"\n(d)ep:\t ExplosionPower (Fireballs)"
	"\n(d)l:\t  Life (FireworksRocketEntity)"
	"\n(d)lt:\t  LifeTime (FireworksRocketEntity)","label"),
	("Misc Params","title")),
	
	(("(d)"
	"\n Prefixing any of the parameters with \"d\"\n allows it to be used on the %s sign to set\n a value on the %d sign."
	"\n Doing this will overwrite the parameter if it's\n also on the %d sign."
	"\n_______________________________________"
	"\n[a:max] will set the max possible (32m18s)"
	"\n[bt:max] will set the max possible (27m18s)"
	"\n[fr:max] will set the max possible (27m18s)"
	"\n[md:max] will set the max possible (27m18s)"
	"\n[xd:max] will set the max possible (27m18s)"
	"\n xd & md: if only one is set, then xd=md"
	"\n\n'm' can be substituted for 'max'"
	"\n_______________________________________"
	"\nCheck the Chunk Format page on the wiki"
	"\nfor more information on parameters"
	"\n\n\t http://bit.ly/chunkformat","label"),
	("(d) & Notes","title")),
	]
	
destinations = []
sources = []
mids = []
spawnerlist = {}

def toByte(val):
	return (127 if val >= 127 else (-128 if val <= -128 else val))
	
def toShort(val):
	return (32767 if val >= 32767 else (-32768 if val <= -32768 else val))

def toInt(val):
	return (2147483647 if val >= 2147483647 else (-2147483648 if val <= -2147483648 else val))
	
def FindID(val):
	for dest in destinations:
		ids = dest["id"].split(",")
		if not ids:
			if dest["id"] == val:
				return dest
		else:
			if val in ids:
				return dest
	if not dests:
		return None

def Spawner2Command(entity):
	command = ""
	if type(entity) is TAG_List:
		list = True
	else:
		list = False

	for tag in range(0,len(entity)) if list else entity.keys():
		if type(entity[tag]) is TAG_Compound:
			if not list:
				if tag != "":
					command += tag+":"
			command += "{"
			command += Spawner2Command(entity[tag])
			command += "}"
		elif type(entity[tag]) is TAG_List:
			if not list:
				if tag != "":
					command += tag+":"
			command += "["
			command += Spawner2Command(entity[tag])
			command += "]"
		else:
			if type(entity[tag]) is TAG_String:
				if entity[tag].value == "":
					continue
			if not list:
				if tag != "":
					command += tag+":"
			if type(entity[tag]) is TAG_String:
				command += "\""
				command += str.replace(entity[tag].value.encode("unicode-escape"), r'"',r'\\"')
				command += "\""
			else:
				command += entity[tag].value.encode("unicode-escape") if isinstance(entity[tag].value, unicode) else str(entity[tag].value)
				if type(entity[tag]) is TAG_Byte:
					command += "b"
				elif type(entity[tag]) is TAG_Short:
					command += "s"
				elif type(entity[tag]) is TAG_Long:
					command += "l"
				elif type(entity[tag]) is TAG_Float:
					command += "f"
				elif type(entity[tag]) is TAG_Double:
					command += "d"
			
		command += ","
	else:
		if command != "":
			if command[-1] == ",":
				command = command[:-1]
	return command

def CreateCommandBlock(x,y,z,e,type,relative=False,setblock=False,blockop=None,comcart=False,fullname=False):
	if setblock and type != "FallingSand":
		setblock = False
	spawn = deepcopy(e)
	if relative or "Pos" not in spawn:
		sx = "~"
		sy = "~"
		sz = "~"
	else:
		sx = ""
		sy = ""
		sz = ""
	posx = spawn["Pos"][0].value
	posy = spawn["Pos"][1].value
	posz = spawn["Pos"][2].value
	if relative:
		posx -= x
		posy -= y
		posz -= z

	if relative:
		sx += str(int(posx))
		sy += str(int(posy))
		sz += str(int(posz))
	else:
		sx += "%.2f"%posx
		sy += "%.2f"%posy
		sz += "%.2f"%posz
	del spawn["Pos"]
	
	if "TileEntityData" in spawn:
		if "x" in spawn["TileEntityData"]:
			del spawn["TileEntityData"]["x"]
		if "y" in spawn["TileEntityData"]:
			del spawn["TileEntityData"]["y"]
		if "z" in spawn["TileEntityData"]:
			del spawn["TileEntityData"]["z"]

	if setblock:
		if "TileEntityData" in spawn:
			spawndata = "{"+Spawner2Command(spawn["TileEntityData"])+"}"
		else:
			spawndata = ""
		if blockop == "r":
			blockoperation = "replace"
		elif blockop == "d":
			blockoperation = "destroy"
		elif blockop == "k":
			blockoperation = "keep"
		else:
			blockoperation = "replace"
		if "TileID" in spawn:
			tile = spawn["TileID"].value
		elif "Tile" in spawn:
			tile = spawn["Tile"].value
		else:
			tile = 1
		if tile in block_map:
			tile = block_map[spawn["TileID"].value]
			if not fullname:
				tile = tile[10:]
		if "Data" in spawn:
			data = spawn["Data"].value
		else:
			data = 0
		
	else:
		spawndata = "{"+Spawner2Command(spawn)+"}"
	newcommand = TAG_Compound()
	if comcart:
		newcommand["id"] = TAG_String("MinecartCommandBlock")
		newcommand["Pos"] = TAG_List([TAG_Double(x+0.5),TAG_Double(y+0.5),TAG_Double(z+0.5)])
		newcommand["Rotation"] = TAG_List([TAG_Float(0.0),TAG_Float(0.0)])
		newcommand["TrackOutput"] = TAG_Byte(0)
		newcommand["SuccessCount"] = TAG_Int(0)
		newcommand["OnGround"] = TAG_Byte(1)
		newcommand["Motion"] = TAG_List([TAG_Double(0.0),TAG_Double(0.0),TAG_Double(0.0)])
		if setblock:
			newcommand["Command"] = TAG_String(unicode("setblock {} {} {} {} {} {} {}".format(unicode(sx), unicode(sy), unicode(sz), unicode(tile), unicode(data), unicode(blockoperation), unicode(spawndata)).decode("unicode-escape")))
		else:
			newcommand["Command"] = TAG_String(unicode("summon {} {} {} {} {}".format(unicode(type), unicode(sx), unicode(sy), unicode(sz), unicode(spawndata)).decode("unicode-escape")))
	else:
		newcommand["id"] = TAG_String("Control")
		newcommand["x"] = TAG_Int(x)
		newcommand["y"] = TAG_Int(y)
		newcommand["z"] = TAG_Int(z)
		newcommand["TrackOutput"] = TAG_Byte(0)
		newcommand["SuccessCount"] = TAG_Int(0)
		if setblock:
			newcommand["Command"] = TAG_String(unicode("setblock {} {} {} {} {} {} {}".format(unicode(sx), unicode(sy), unicode(sz), unicode(tile), unicode(data), unicode(blockoperation), unicode(spawndata)).decode("unicode-escape")))
		else:
			newcommand["Command"] = TAG_String(unicode("summon {} {} {} {} {}".format(unicode(type), unicode(sx), unicode(sy), unicode(sz), unicode(spawndata)).decode("unicode-escape")))
	return newcommand

def perform(level, box, options):
	op = options["Operation:"]
	fullname = options["Use full block name for setblock commands"]
	removesigns = options["Remove Signs Upon Completion"]
	removeblocks = options["Remove Blocks\\Entities Upon Completion (midway signs only)"]
	find = options["Find\\Remove Variable:"]
	replace = options["Replace\\Add Variable:"]

				
	def ParseInnerParams(spwn, listitem):
		if "i" in listitem:
			spwn["Invulnerable"] = TAG_Byte(1)
		else:
			spwn["Invulnerable"] = TAG_Byte(0)

		if "fr" in listitem:
			if listitem["fr"][0] == "m":
				spwn["Fire"] = TAG_Short(32767)
			else:
				spwn["Fire"] = TAG_Short(toShort(int(listitem["fr"])))
		else:
			spwn["Fire"] = TAG_Short(-1)

		if "fd" in listitem:
			spwn["FallDistance"] = TAG_Float(float(listitem["fd"]))
		else:
			spwn["FallDistance"] = TAG_Float(0.0)

		if "yw" in listitem or "ph" in listitem:
			spwn["Rotation"] = TAG_List()
			if "yw" in listitem:
				spwn["Rotation"].append(TAG_Float(float(listitem["yw"])))
			else:
				spwn["Rotation"].append(TAG_Float(0.0))
			if "ph" in listitem:
				spwn["Rotation"].append(TAG_Float(float(listitem["ph"])))
			else:
				spwn["Rotation"].append(TAG_Float(0.0))
			
		if "vx" in listitem or "vy" in listitem or "vz" in listitem:
			spwn["Motion"] = TAG_List()
			if "vx" in listitem:
				spwn["Motion"].append(TAG_Double(float(listitem["vx"])))
			else:
				spwn["Motion"].append(TAG_Double(0.0))
			if "vy" in listitem:
				spwn["Motion"].append(TAG_Double(float(listitem["vy"])))
			else:
				spwn["Motion"].append(TAG_Double(0.0))
			if "vz" in listitem:
				spwn["Motion"].append(TAG_Double(float(listitem["vz"])))
			else:
				spwn["Motion"].append(TAG_Double(0.0))

	def ParseInnerDestParams(spwn, listitem):
		if "di" in listitem:
			spwn["Invulnerable"] = TAG_Byte(1)
			
		if "dfr" in listitem:
			if listitem["dfr"][0] == "m":
				spwn["Fire"] = TAG_Short(32767)
			else:
				spwn["Fire"] = TAG_Short(toShort(int(listitem["dfr"])))

		if "dfd" in listitem:
			spwn["FallDistance"] = TAG_Float(float(listitem["dfd"]))

		if "dyw" in listitem or "dph" in listitem:
			spwn["Rotation"] = TAG_List()
			if "dyw" in listitem:
				spwn["Rotation"].append(TAG_Float(float(listitem["dyw"])))
			else:
				spwn["Rotation"].append(TAG_Float(0.0))
			if "dph" in listitem:
				spwn["Rotation"].append(TAG_Float(float(listitem["dph"])))
			else:
				spwn["Rotation"].append(TAG_Float(0.0))
				
		if "dvx" in listitem or "dvy" in listitem or "dvz" in listitem:
			spwn["Motion"] = TAG_List()
			if "dvx" in listitem:
				spwn["Motion"].append(TAG_Double(float(listitem["dvx"])))
			else:
				spwn["Motion"].append(TAG_Double(0.0))
			if "dvy" in listitem:
				spwn["Motion"].append(TAG_Double(float(listitem["dvy"])))
			else:
				spwn["Motion"].append(TAG_Double(0.0))
			if "dvz" in listitem:
				spwn["Motion"].append(TAG_Double(float(listitem["dvz"])))
			else:
				spwn["Motion"].append(TAG_Double(0.0))

	if op == "Populate Sign TileEntities":
		for x in xrange(box.minx, box.maxx):
			for z in xrange(box.minz, box.maxz):
				for y in xrange(box.miny, box.maxy):
					block = level.blockAt(x,y,z)
					if block == 63 or block == 68:
						t = level.tileEntityAt(x,y,z)
						if t == None:
							sign = TAG_Compound()
							sign["id"] = TAG_String("Sign")
							sign["x"] = TAG_Int(x)
							sign["y"] = TAG_Int(y)
							sign["z"] = TAG_Int(z)
							sign["Text1"] = TAG_String()
							sign["Text2"] = TAG_String()
							sign["Text3"] = TAG_String()
							sign["Text4"] = TAG_String()
							chunk = level.getChunk(x>>4, z>>4)
							chunk.TileEntities.append(sign)
							chunk.dirty = True
		return
	elif "Convert Signs" in op:
		for x in xrange(box.minx, box.maxx):
			for z in xrange(box.minz, box.maxz):
				for y in xrange(box.miny, box.maxy):
					block = level.blockAt(x,y,z)
					if op == "Convert Signs: Wall -> Standing" and block == 68:
						data = level.blockDataAt(x,y,z)
						if data == 2:
							newdata = 8
						elif data == 3:
							newdata = 0
						elif data == 4:
							newdata = 4
						elif data == 5:
							newdata = 12
						level.setBlockAt(x, y, z, 63)
						level.setBlockDataAt(x, y, z, newdata)
					elif op == "Convert Signs: Standing -> Wall" and block == 63:
						data = level.blockDataAt(x,y,z)
						if data in (6,7,8,9,10):
							if data == 6:
								if level.blockAt(x+1,y,z) != 0:
									newdata = 5
								elif level.blockAt(x,y,z-1) != 0:
									newdata = 3
							elif data == 10:
								if level.blockAt(x-1,y,z) != 0:
									newdata = 4
								elif level.blockAt(x,y,z-1) != 0:
									newdata = 3
							else:
								newdata = 2
						elif data in (0,1,2,14,15):
							if data == 2:
								if level.blockAt(x+1,y,z) != 0:
									newdata = 5
								elif level.blockAt(x,y,z+1) != 0:
									newdata = 2
							elif data == 14:
								if level.blockAt(x-1,y,z) != 0:
									newdata = 4
								elif level.blockAt(x,y,z+1) != 0:
									newdata = 2
							else:
								newdata = 3
						elif data in (3,4,5):
							newdata = 4
						elif data in (11,12,13):
							newdata = 5
						level.setBlockAt(x, y, z, 68)
						level.setBlockDataAt(x, y, z, newdata)
		return
	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:
				if e["id"].value != "Sign":
					continue
				if op == "Find\\Replace Sign Text":
					if find == "" or find == "NONE":
						if replace == "" or replace == "NONE":
							return
						for textitems in ("Text1", "Text2", "Text3", "Text4"):
							if textitems in e:
								text = e[textitems].value
								leng = len(text)
								if leng > 0:
									if text[-1] != " ":
										leng += 1
								if (len(replace) + leng) <= 15:
									newstr = e[textitems].value
									if leng > 0:
										if text[-1] != " ":
											newstr += " "
									newstr += replace
									newstr = re.sub("\\s{2,}", " ", newstr)
									e[textitems] = TAG_String(newstr)
									chunk.dirty = True				
									break
							else:
								e[textitems] = TAG_String(replace)
								chunk.dirty = True				
								break
					else:
						if replace == "" or replace == "NONE":
							replacestr = ""
						else:
							replacestr = replace
						if find[-1] == ":":
							if ":" in replacestr:
								if find.split(":")[0] != replacestr.split(":")[0]:
									continue
							elif replacestr != "":
								continue

							for textitems in ("Text1", "Text2", "Text3", "Text4"):
								if textitems in e:
									text = e[textitems].value
									temp = text.split(" ")
									ps = {}
									for p in temp:
										if p != "":
											key, val = p.partition(":")[::2]
											ps[key] = val
									if find[:-1] in ps:
										if replacestr == "":
											del ps[find[:-1]]
										else:
											ps[find[:-1]] = replacestr.partition(":")[-1]
										newstr = " ".join(["%s:%s" % (key, value) for (key, value) in sorted(ps.items())])
										newstr = re.sub("\\s{2,}", " ", newstr)
										e[textitems] = TAG_String(newstr)
										chunk.dirty = True
										break
						else:
							for textitems in ("Text1", "Text2", "Text3", "Text4"):
								if textitems in e:
									text = e[textitems].value
									if text.find(find) != -1:
										text = unicode.replace(text,find,replacestr)
										text = re.sub("\\s{2,}", " ", text)
										if len(text) > 1:
											if text[0] == " ":
												text = text[1:]
										e[textitems] = TAG_String(text)
										chunk.dirty = True
										break
					continue
				elif op == "Empty All Sign Text":
					if "Text1" in e:
						del e["Text1"]
					if "Text2" in e:
						del e["Text2"]
					if "Text3" in e:
						del e["Text3"]
					if "Text4" in e:
						del e["Text4"]
					e["Text1"] = TAG_String()
					e["Text2"] = TAG_String()
					e["Text3"] = TAG_String()
					e["Text4"] = TAG_String()
					chunk.dirty = True
					continue
				text = ""
				if "Text1" in e:
					text += e["Text1"].value.lower() + " "
				if "Text2" in e:
					text += e["Text2"].value.lower() + " "
				if "Text3" in e:
					text += e["Text3"].value.lower() + " "
				if "Text4" in e:
					text += e["Text4"].value.lower() + " "
				temp = text.split(" ")
				pairs = {}
				for p in temp:
					if p != "":
						key, val = p.partition(":")[::2]
						pairs[key] = val
				pairs["obj"] = e
				pairs["chunk"] = chunk
				if "id" not in pairs and "%m" not in pairs and "%s" not in pairs and "%d" not in pairs:
					print "No ID found in sign"
					continue
				if "src" in pairs or "%s" in pairs:
					if "id" not in pairs:
						pairs["id"] = pairs["%s"]
					sources.append(pairs)
				elif "dest" in pairs or "%d" in pairs:
					if "id" not in pairs:
						pairs["id"] = pairs["%d"]
					destinations.append(pairs)
				elif "midway" in pairs or "%m" in pairs:
					if "id" not in pairs:
						pairs["id"] = pairs["%m"]
					pairs["count"] = 0
					mids.append(pairs)
	if op == "Replace Sign Text" or op == "Clear Sign Text":
		return

	for m in mids:
		for src in sources:
			if "%m" in src:
				if m["id"] == src["%m"]:
					m["count"] += 1
					src["midwayobj"] = m
	
	placed = False
	setblock = False
	
	for src in sources:
		if "sx" in src:
			srcx = int(src["sx"])
		else:
			srcx = 0
		if "sy" in src:
			srcy = int(src["sy"])
		else:
			if "sx" not in src and "sz" not in src:
				srcy = -1
			else:
				srcy = 0
		if "sz" in src:
			srcz = int(src["sz"])
		else:
			srcz = 0

		x = src["obj"]["x"].value
		y = src["obj"]["y"].value
		z = src["obj"]["z"].value

		cart = TAG_Compound()
		cart["Rotation"] = TAG_List()
		cart["Rotation"].append(TAG_Float(0.0))
		cart["Rotation"].append(TAG_Float(0.0))

		cart["Pos"] = TAG_List()
		
		if "rel" in src:
			relative = True
		else:
			relative = False
		
		if "%m" in src:
			if "midwayobj" not in src:
				continue
			cx = src["midwayobj"]["obj"]["x"].value + 0.5
			cy = src["midwayobj"]["obj"]["y"].value + 0.5
			cz = src["midwayobj"]["obj"]["z"].value + 0.5
			if "x" in src:
				cx += float(src["x"])
			if "y" in src:
				cy += float(src["y"])
			if "z" in src:
				cz += float(src["z"])
			if "rel" in src:
				cx -= x
				cy -= y
				cz -= z
			cart["Pos"].append(TAG_Double(cx))
			cart["Pos"].append(TAG_Double(cy))
			cart["Pos"].append(TAG_Double(cz))
		
		if "ent" in src:
			cart["DisplayTile"] = TAG_Int(55)
			cart["DisplayData"] = TAG_Int(0)
			cart["CustomDisplayTile"] = TAG_Byte(1)
			ox = x + srcx - 1
			oy = y + srcy - 3
			oz = z + srcz - 1
			tileent = False
			tent = level.tileEntityAt(x+srcz,y+srcy,z+srcz)
			if tent != None:
				if "Items" in tent:
					if len(tent["Items"]) > 0:
						ent = TAG_Compound()
						ent["id"] = TAG_String("Item")
						if len(tent["Items"]) == 1:
							if tent["Items"][0]["id"].value == 401 and "fw" in src:
								ent["id"] = TAG_String("FireworksRocketEntity")
								ent["FireworksItem"] = deepcopy(tent["Items"][0])
								if "Slot" in ent["FireworksItem"]:
									del ent["FireworksItem"]["Slot"]
							else:
								ent["Item"] = deepcopy(tent["Items"][0])
								if "Slot" in ent["Item"]:
									del ent["Item"]["Slot"]
						else:
							entptr = ent
							for item in tent["Items"]:
								entptr["FallDistance"] = TAG_Float(0.0)
								entptr["Fire"] = TAG_Short(-1)
								entptr["Item"] = deepcopy(item)
								entptr["id"] = TAG_String("Item")
								if "Slot" in entptr["Item"]:
									del entptr["Item"]["Slot"]
								entptr["Riding"] = TAG_Compound()
								entptr = entptr["Riding"]
						tileent = True
				elif tent["id"].value == "MobSpawner":
					if "SpawnData" in tent:
						ent = deepcopy(tent["SpawnData"])
						ent["id"] = TAG_String(tent["EntityId"].value)
						tileent = True
					elif "SpawnPotentials" in tent:
						if len(tent["SpawnPotentials"]) > 0:
							ent = deepcopy(tent["SpawnPotentials"][0]["Properties"])
							ent["id"] = TAG_String(tent["SpawnPotentials"][0]["Type"].value)
							tileent = True
					else:
						ent = TAG_Compound()
						ent["id"] = TAG_String(tent["EntityId"].value)
						tileent = True
			if not tileent:
				searchbox = BoundingBox((ox,oy,oz),(3,4,3))
				ents = level.getEntitiesInBox(searchbox)
				if not ents:
					print "Error! No Entity found for source sign at", x, y, z
					continue
				else:
					ent = deepcopy(ents[0])
					if len(ents) > 1:
						entptr = ent
						if "Pos" in entptr:
							del entptr["Pos"]
						for item in ents:
							if ents.index(item) == 0:
								continue
							entptr["Riding"] = deepcopy(item)
							if "Pos" in entptr["Riding"]:
								del entptr["Riding"]["Pos"]
							entptr = entptr["Riding"]
			# if "UUIDMost" in ent:
				# del ent["UUIDMost"]
			# if "UUIDLeast" in ent:
				# del ent["UUIDLeast"]
			dest = FindID(src["id"])
			if dest == None:
				print "Error! No matching destination sign found within selection for sign at", x, y, z
				continue

			cart["EntityId"] = TAG_String(ent["id"].value)
			cart["SpawnData"] = TAG_Compound()
			cart["SpawnData"] = deepcopy(ent)
			sx = dest["obj"]["x"].value+0.5
			sy = dest["obj"]["y"].value+0.5
			sz = dest["obj"]["z"].value+0.5
			ParseInnerParams(cart["SpawnData"],dest)
			ParseInnerDestParams(cart["SpawnData"],src)
			
			if cart["EntityId"].value == "Item":
				if "a" in dest:
					if dest["a"][0] == "m":
						cart["SpawnData"]["Age"] = TAG_Short(-32768)
					else:
						cart["SpawnData"]["Age"] = TAG_Short(toShort(int(dest["a"])))
				if "da" in src:
					if src["da"][0] == "m":
						cart["SpawnData"]["Age"] = TAG_Short(-32768)
					else:
						cart["SpawnData"]["Age"] = TAG_Short(toShort(int(src["da"])))

			if cart["EntityId"].value == "FireworksRocketEntity":
				if "l" in dest:
					if dest["l"][0] == "m":
						cart["SpawnData"]["Life"] = TAG_Int(2147483647)
					else:
						cart["SpawnData"]["Life"] = TAG_Int(toInt(int(dest["l"])))
				if "dl" in src:
					if src["dl"][0] == "m":
						cart["SpawnData"]["Life"] = TAG_Int(2147483647)
					else:
						cart["SpawnData"]["Life"] = TAG_Int(toInt(int(src["dl"])))
				if "lt" in dest:
					if dest["lt"][0] == "m":
						cart["SpawnData"]["LifeTime"] = TAG_Int(2147483647)
					else:
						cart["SpawnData"]["LifeTime"] = TAG_Int(toInt(int(dest["lt"])))
				if "dlt" in src:
					if src["dlt"][0] == "m":
						cart["SpawnData"]["LifeTime"] = TAG_Int(2147483647)
					else:
						cart["SpawnData"]["LifeTime"] = TAG_Int(toInt(int(src["dlt"])))

			if cart["EntityId"].value == "PrimedTnt":
				if "fs" in dest:
					if dest["fs"][0] == "m":
						cart["SpawnData"]["Fuse"] = TAG_Byte(127)
					else:
						cart["SpawnData"]["Fuse"] = TAG_Byte(toByte(int(dest["fs"])))
				if "dfs" in src:
					if src["dfs"][0] == "m":
						cart["SpawnData"]["Fuse"] = TAG_Byte(127)
					else:
						cart["SpawnData"]["Fuse"] = TAG_Byte(toByte(int(src["dfs"])))
				if "er" in dest:
					if dest["er"][0] == "m":
						cart["SpawnData"]["ExplosionRadius"] = TAG_Byte(127)
					else:
						cart["SpawnData"]["ExplosionRadius"] = TAG_Byte(toByte(int(dest["er"])))
				if "der" in src:
					if src["der"][0] == "m":
						cart["SpawnData"]["ExplosionRadius"] = TAG_Byte(127)
					else:
						cart["SpawnData"]["ExplosionRadius"] = TAG_Byte(toByte(int(src["der"])))

			if cart["EntityId"].value == "Fireball":
				if "ep" in dest:
					if dest["ep"][0] == "m":
						cart["SpawnData"]["ExplosionPower"] = TAG_Int(2147483647)
					else:
						cart["SpawnData"]["ExplosionPower"] = TAG_Int(toInt(int(dest["ep"])))
				if "dep" in src:
					if src["dep"][0] == "m":
						cart["SpawnData"]["ExplosionPower"] = TAG_Int(2147483647)
					else:
						cart["SpawnData"]["ExplosionPower"] = TAG_Int(toInt(int(src["dep"])))
						
			if "x" in dest:
				sx += float(dest["x"])
			if "y" in dest:
				sy += float(dest["y"])
			if "z" in dest:
				sz += float(dest["z"])
				
			if "dx" in src:
				sx  = dest["obj"]["x"].value+0.5 + float(src["dx"])
			if "dy" in src:
				sy  = dest["obj"]["y"].value+0.5 + float(src["dy"])
			if "dz" in src:
				sz  = dest["obj"]["z"].value+0.5 + float(src["dz"])
				
			if "Pos" in cart["SpawnData"]:
				del cart["SpawnData"]["Pos"]
			cart["SpawnData"]["Pos"] = TAG_List()
			cart["SpawnData"]["Pos"].append(TAG_Double(sx))
			cart["SpawnData"]["Pos"].append(TAG_Double(sy))
			cart["SpawnData"]["Pos"].append(TAG_Double(sz))

			dest["CanDelete"] = True

			chnk = level.getChunk(x>>4,z>>4)

			combstack = False
			if "midwayobj" in src:
				combstack = True
			
			if combstack:
				idval = src["midwayobj"]["id"]
				if idval not in spawnerlist:
					spawnerlist[idval] = {}
					spawnerlist[idval]["master"] = src["midwayobj"]
				if "%smain" in src:
					spawnerlist[idval]["mainsign"] = src
				spawnerlist[idval]["spawner"] = cart
				spawnerlist[idval]["setblock"] = False
				spawnerlist[idval]["operation"] = None
				if "rel" in src:
					spawnerlist[idval]["relative"] = True
				else:
					spawnerlist[idval]["relative"] = False

				if removeblocks:
					if tileent:
						chnk.TileEntities.remove(tent)
					else:
						level.removeEntitiesInBox(searchbox)
					level.setBlockAt(x+srcx, y+srcy, z+srcz, 0)
					level.setBlockDataAt(x+srcx, y+srcy, z+srcz, 0)
			else:
				if tileent:
					chnk.TileEntities.remove(tent)
				else:
					level.removeEntitiesInBox(searchbox)
				bx = x+srcx
				by = y+srcy
				bz = z+srcz
				if "cart" in src:
					chnk.Entities.append(CreateCommandBlock(bx,by,bz,cart["SpawnData"],cart["EntityId"].value,relative, False, None, True, fullname))
					level.setBlockAt(bx, by, bz, 157)
					level.setBlockDataAt(bx, by, bz, 0)
				else:
					chnk.TileEntities.append(CreateCommandBlock(bx,by,bz,cart["SpawnData"],cart["EntityId"].value,relative, False, None, False, fullname))
					level.setBlockAt(bx, by, bz, 137)
					level.setBlockDataAt(bx, by, bz, 0)
				chnk.dirty = True
			src["CanDelete"] = True
			if "midwayobj" in src:
				src["midwayobj"]["CanDelete"] = True
		else:
			fallsand = True
			block = level.blockAt(x+srcx, y+srcy, z+srcz)
			data = level.blockDataAt(x+srcx, y+srcy, z+srcz)
			cart["DisplayTile"] = TAG_Int(block)
			cart["DisplayData"] = TAG_Int(data)
			cart["CustomDisplayTile"] = TAG_Byte(1)
			tent = level.tileEntityAt(x+srcx,y+srcy,z+srcz)
			if block == 0:
				print "Error! Could not find non-air block for source sign at", x, y, z
				continue
			dest = FindID(src["id"])
			if dest == None:
				print "Error! No matching destination sign found within selection for sign at", x, y, z
				continue

			cart["EntityId"] = TAG_String("FallingSand")
			cart["SpawnData"] = TAG_Compound()
			cart["SpawnData"]["TileID"] = TAG_Int(block)
			cart["SpawnData"]["Data"] = TAG_Byte(data)
			if tent != None:
				cart["SpawnData"]["TileEntityData"] = deepcopy(tent)
			sx = dest["obj"]["x"].value+0.5
			sy = dest["obj"]["y"].value+0.5
			sz = dest["obj"]["z"].value+0.5
			ParseInnerParams(cart["SpawnData"],dest)
			ParseInnerDestParams(cart["SpawnData"],src)

			if "t" in dest:
				if dest["t"][0] == "m":
					cart["SpawnData"]["Time"] = TAG_Byte(127)
				else:
					cart["SpawnData"]["Time"] = TAG_Byte(toByte(int(dest["t"])))
			else:
				cart["SpawnData"]["Time"] = TAG_Byte(2)
			if "dt" in src:
				if src["dt"][0] == "m":
					cart["SpawnData"]["Time"] = TAG_Byte(127)
				else:
					cart["SpawnData"]["Time"] = TAG_Byte(toByte(int(src["dt"])))

			if "dr" in dest:
				cart["SpawnData"]["DropItem"] = TAG_Byte(1)
			elif "ddr" in src:
				cart["SpawnData"]["DropItem"] = TAG_Byte(1)			
			else:
				cart["SpawnData"]["DropItem"] = TAG_Byte(0)

			if "h" in dest:
				cart["SpawnData"]["HurtEntities"] = TAG_Byte(1)
			elif "dh" in src:
				cart["SpawnData"]["HurtEntities"] = TAG_Byte(1)
			else:
				cart["SpawnData"]["HurtEntities"] = TAG_Byte(0)

			if "hm" in dest:
				if dest["hm"][0] == "m":
					cart["SpawnData"]["FallHurtMax"] = TAG_Int(2147483647)
				else:
					cart["SpawnData"]["FallHurtMax"] = TAG_Int(toInt(int(dest["hm"])))
			if "ha" in dest:
				if dest["ha"][0] == "m":
					cart["SpawnData"]["FallHurtAmount"] = TAG_Float(2147483647.0)
				else:
					cart["SpawnData"]["FallHurtAmount"] = TAG_Float(toInt(int(dest["ha"])))

			if "dhm" in src:
				if src["dhm"][0] == "m":
					cart["SpawnData"]["FallHurtMax"] = TAG_Int(2147483647)
				else:
					cart["SpawnData"]["FallHurtMax"] = TAG_Int(toInt(int(src["dhm"])))
			if "dha" in src:
				if src["dha"][0] == "m":
					cart["SpawnData"]["FallHurtAmount"] = TAG_Float(2147483647.0)
				else:
					cart["SpawnData"]["FallHurtAmount"] = TAG_Float(toInt(int(src["dha"])))
					
			if tent != None:
				if tent["id"].value == "Furnace":
					if "bt" in dest:
						if dest["bt"][0] == "m":
							cart["SpawnData"]["TileEntityData"]["BurnTime"] = TAG_Short(32767)
						else:
							cart["SpawnData"]["TileEntityData"]["BurnTime"] = TAG_Short(toShort(int(dest["bt"])))
					if "dbt" in src:
						if src["dbt"][0] == "m":
							cart["SpawnData"]["TileEntityData"]["BurnTime"] = TAG_Short(32767)
						else:
							cart["SpawnData"]["TileEntityData"]["BurnTime"] = TAG_Short(toShort(int(src["dbt"])))

			if "x" in dest:
				sx += float(dest["x"])
			if "y" in dest:
				sy += float(dest["y"])
			if "z" in dest:
				sz += float(dest["z"])

			if "dx" in src:
				sx  = dest["obj"]["x"].value+0.5 + float(src["dx"])
			if "dy" in src:
				sy  = dest["obj"]["y"].value+0.5 + float(src["dy"])
			if "dz" in src:
				sz  = dest["obj"]["z"].value+0.5 + float(src["dz"])

			if "Pos" in cart["SpawnData"]:
				del cart["SpawnData"]["Pos"]
			cart["SpawnData"]["Pos"] = TAG_List()

			cart["SpawnData"]["Pos"].append(TAG_Double(sx))
			cart["SpawnData"]["Pos"].append(TAG_Double(sy))
			cart["SpawnData"]["Pos"].append(TAG_Double(sz))

			dest["CanDelete"] = True
				
			chnk = level.getChunk(x>>4,z>>4)
			
			blockop = None
			if "set" in src:
				if src["set"][0] in "rkd":
					blockop = src["set"][0]
				else:
					blockop = "r"
				setblock = True
			else:
				setblock = False
			
			combstack = False
			if "midwayobj" in src:
				combstack = True

			if combstack:
				idval = src["midwayobj"]["id"]
				if idval not in spawnerlist:
					spawnerlist[idval] = {}
					spawnerlist[idval]["master"] = src["midwayobj"]
				if "%smain" in src:
					spawnerlist[idval]["mainsign"] = src
				spawnerlist[idval]["spawner"] = cart
				spawnerlist[idval]["setblock"] = setblock
				spawnerlist[idval]["operation"] = blockop
				if "rel" in src:
					spawnerlist[idval]["relative"] = True
				else:
					spawnerlist[idval]["relative"] = False

				if removeblocks:
					if tent != None:
						chnk.TileEntities.remove(tent)
					level.setBlockAt(x+srcx, y+srcy, z+srcz, 0)
					level.setBlockDataAt(x+srcx, y+srcy, z+srcz, 0)
			else:
				if tent != None:
					chnk.TileEntities.remove(tent)
				bx = x+srcx
				by = y+srcy
				bz = z+srcz
				if "cart" in src:
					chnk.Entities.append(CreateCommandBlock(bx,by,bz,cart["SpawnData"],cart["EntityId"].value,relative, setblock, blockop, True, fullname))
					level.setBlockAt(bx, by, bz, 157)
					level.setBlockDataAt(bx, by, bz, 0)
				else:
					chnk.TileEntities.append(CreateCommandBlock(bx,by,bz,cart["SpawnData"],cart["EntityId"].value,relative, setblock, blockop, False, fullname))
					level.setBlockAt(bx, by, bz, 137)
					level.setBlockDataAt(bx, by, bz, 0)
				chnk.dirty = True
			src["CanDelete"] = True
			if "midwayobj" in src:
				src["midwayobj"]["CanDelete"] = True
	
	# if placeholder and not combstack and not commandblock:
		# CreatePlaceholder(cart["Pos"][0].value,cart["Pos"][1].value,cart["Pos"][2].value)
	for key in spawnerlist.keys():
		if "mainsign" in spawnerlist[key]:
			if "sx" in spawnerlist[key]["mainsign"]:
				srcx = int(spawnerlist[key]["mainsign"]["sx"])
			else:
				srcx = 0
			if "sy" in spawnerlist[key]["mainsign"]:
				srcy = int(spawnerlist[key]["mainsign"]["sy"])
			else:
				srcy = -1
			if "sz" in spawnerlist[key]["mainsign"]:
				srcz = int(spawnerlist[key]["mainsign"]["sz"])
			else:
				srcz = 0
			x = spawnerlist[key]["mainsign"]["obj"]["x"].value + srcx
			y = spawnerlist[key]["mainsign"]["obj"]["y"].value + srcy
			z = spawnerlist[key]["mainsign"]["obj"]["z"].value + srcz

			if "x" in spawnerlist[key]["mainsign"]:
				ox = float(float(spawnerlist[key]["mainsign"]["x"]) + x)
			else:
				ox = None
			if "y" in spawnerlist[key]["mainsign"]:
				oy = float(float(spawnerlist[key]["mainsign"]["y"]) + y)
			else:
				oy = None
			if "z" in spawnerlist[key]["mainsign"]:
				oz = float(float(spawnerlist[key]["mainsign"]["z"]) + z)
			else:
				oz = None
		else:
			if "sx" in spawnerlist[key]["master"]:
				srcx = int(spawnerlist[key]["master"]["sx"])
			else:
				srcx = 0
			if "sy" in spawnerlist[key]["master"]:
				srcy = int(spawnerlist[key]["master"]["sy"])
			else:
				srcy = -1
			if "sz" in spawnerlist[key]["master"]:
				srcz = int(spawnerlist[key]["master"]["sz"])
			else:
				srcz = 0
			x = spawnerlist[key]["master"]["obj"]["x"].value + srcx
			y = spawnerlist[key]["master"]["obj"]["y"].value + srcy
			z = spawnerlist[key]["master"]["obj"]["z"].value + srcz

			if "x" in spawnerlist[key]["master"]:
				ox = float(float(spawnerlist[key]["master"]["x"]) + x)
			else:
				ox = None
			if "y" in spawnerlist[key]["master"]:
				oy = float(float(spawnerlist[key]["master"]["y"]) + y)
			else:
				oy = None
			if "z" in spawnerlist[key]["master"]:
				oz = float(float(spawnerlist[key]["master"]["z"]) + z)
			else:
				oz = None

		cart = spawnerlist[idval]["spawner"]
		setblock = spawnerlist[idval]["setblock"]
		blockop = spawnerlist[idval]["operation"]
		relative = spawnerlist[idval]["relative"]
		bx = cart["Pos"][0].value
		by = cart["Pos"][0].value
		bz = cart["Pos"][0].value

		chnk = level.getChunk(int(bx)>>4,int(bz)>>4)
		chnk.Entities.append(CreateCommandBlock(bx,by,bz,cart["SpawnData"],cart["EntityId"].value,relative, setblock, blockop, True, fullname))

		chnk.dirty = True
		
		
	if removesigns:
		for src in sources:
			if "CanDelete" in src:
				if src["CanDelete"]:
					x = src["obj"]["x"].value
					y = src["obj"]["y"].value
					z = src["obj"]["z"].value
					level.setBlockAt(x, y, z, 0)
					level.setBlockDataAt(x, y, z, 0)
					src["chunk"].TileEntities.remove(src["obj"])
					src["chunk"].dirty = True
		for dest in destinations:
			if "CanDelete" in dest:
				if dest["CanDelete"]:
					x = dest["obj"]["x"].value
					y = dest["obj"]["y"].value
					z = dest["obj"]["z"].value
					level.setBlockAt(x, y, z, 0)
					level.setBlockDataAt(x, y, z, 0)
					dest["chunk"].TileEntities.remove(dest["obj"])
					dest["chunk"].dirty = True
		for m in mids:
			if "CanDelete" in m:
				if m["CanDelete"]:
					x = m["obj"]["x"].value
					y = m["obj"]["y"].value
					z = m["obj"]["z"].value
					level.setBlockAt(x, y, z, 0)
					level.setBlockDataAt(x, y, z, 0)
					m["chunk"].TileEntities.remove(m["obj"])
					m["chunk"].dirty = True
