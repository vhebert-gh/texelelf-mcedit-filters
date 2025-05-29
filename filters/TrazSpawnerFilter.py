from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float, TAG_Byte_Array, TAG_Int_Array
from pymclevel import BoundingBox
from copy import deepcopy
import random
import re
import operator

displayName = "TrazLander's Spawner Filter"

sorts = {"Y, X, Z":(1,0,2), "Y, Z, X":(1,2,0),"X, Y, Z":(0,1,2), "Z, Y, X":(2,1,0), "X, Z, Y":(0,2,1), "Z, X, Y":(2,0,1)}
ascdescx = {"Ascending (-X to +X)":1,"Descending (+X to -X)":-1}
ascdescy = {"Ascending (-Y to +Y)":1,"Descending (+Y to -Y)":-1}
ascdescz = {"Ascending (-Z to +Z)":1,"Descending (+Z to -Z)":-1}

inputs = [
	(("Delay", (0,-32768,32767)),
	("MinSpawnDelay",(10,0,32767)),
	("MaxSpawnDelay",(10,0,32767)),
	("RequiredPlayerRange", (32767,0,32767)),
	("Sort Order:",tuple(sorts.keys())),
	("X-axis sort order:",tuple(sorted(ascdescx.keys()))),
	("Y-axis sort order:",tuple(sorted(ascdescy.keys()))),
	("Z-axis sort order:",tuple(sorted(ascdescz.keys()))),
	("Create Spawner Minecart Placeholder", True),
	("Remove Signs Upon Completion",True),
	("Remove Blocks\\Entities Upon Completion (Stack or Combine mode only)",True),
	("Find\\Remove Variable:",("string","value=NONE")),
	("Replace\\Add Variable:",("string","value=NONE")),
	("Operation:",(	"Create Spawners",
					"Find\\Replace Sign Text",
					"Empty All Sign Text",
					"Populate Sign TileEntities",
					"Convert Signs: Wall -> Standing",
					"Convert Signs: Standing -> Wall")),
	("Defaults","title")),

	(("%s:<id>\t Source"
	"\n%d:<id>\t Destination"
	"\n_______________________________________"
	"\n%m:<id> Optional: Midway spawn location\n\t\t-Pair with '%m:<id>' \n\t\t on any %s signs"
	"\nid:<id>  Optional: Unique, case-insensitive ID \n\t\t-Pair with src/dest/midway"
	"\n_______________________________________"
	"\n\nent\t  Add to %s signs:\n\t\t-Spawns projectile/item/mob entity"
	"\nent fw\t Add to %s signs:\n\t\t-Spawns FireworksRocketEntity"
	"\n\ncomb\tAdd to %m signs:\n\t\t-Combines all %s spawners into a\n\t\t single randomized source spawner"
	"\nstack\t Add to %m signs:\n\t\t-Combines all %s spawners into a\n\t\t single stacked entity spawner"
	"\nseth(:)\t Add to %m signs:\n\t\t-SethBling-styled spawning \n\t\t-Optional sort: (e.g. seth:-yx-z)"
	"\n(d)multi  Add to %m OR %d signs:\n\t\t-Will repeat spawning infinitely\n\t\t-Define how fast with md & xd","label"),
	("Base Params","title"),),
	
	(("(d)x: (d)y: (d)z:\tAdds value to Coordinates"
	"\n(d)vx: (d)vy: (d)vz:   Adds value to Velocity"
	"\n(d)yw: (d)ph:\t\tSets Yaw & Pitch Rotation"
	"\n\n(d)t:\t Time FallingSand has existed"
	"\n(d)d:\t Initial Delay"
	"\n(d)md:\tMinSpawnDelay"
	"\n(d)xd:\t MaxSpawnDelay"
	"\n(d)sc:\t SpawnCount of objects to attempt to spawn"
	"\n(d)sr:\t  SpawnRange"
	"\n(d)me:\tMaxNearbyEntities inside of SpawnRange"
	"\n(d)pr:\t RequiredPlayerRange"
	"\n(d)wt:\tWeight: how often it'll be picked to spawn"
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
	"\nSpawnRange"
	"\n Every value increments horizontal spawn range by\n 2 blocks. Vertical is always 4 blocks above and 4\n blocks below."
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
	"\n\n\t http://bit.ly/chunkformat"
	,"label"),
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
	dests = []
	for dest in destinations:
		ids = dest["id"].split(",")
		if not ids:
			if dest["id"] == val:
				dests.append(dest)
		else:
			if val in ids:
				dests.append(dest)
	if not dests:
		return None
	else:
		return dests

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

def CreateCommandBlock(x,y,z,e,type):
	spawn = deepcopy(e)
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
	newcommand = TAG_Compound()
	newcommand["id"] = TAG_String("Control")
	newcommand["x"] = TAG_Int(x)
	newcommand["y"] = TAG_Int(y)
	newcommand["z"] = TAG_Int(z)
	newcommand["SuccessCount"] = TAG_Int(0)
	newcommand["Command"] = TAG_String(unicode("summon {} {} {} {} {}".format(unicode(type), unicode(sx), unicode(sy), unicode(sz), unicode(spawndata)).decode("unicode-escape")))
	return newcommand

def perform(level, box, options):
	op = options["Operation:"]
	defdelay = options["Delay"]
	defmindelay = options["MinSpawnDelay"]
	defmaxdelay = options["MaxSpawnDelay"]
	defnum = 1
	defenties = 1
	defrange = 0
	defradius = options["RequiredPlayerRange"]
	orderx, ordery, orderz = sorts[options["Sort Order:"]]
	xsort = ascdescx[options["X-axis sort order:"]]
	ysort = ascdescy[options["Y-axis sort order:"]]
	zsort = ascdescz[options["Z-axis sort order:"]]
	placeholder = options["Create Spawner Minecart Placeholder"]
	removesigns = options["Remove Signs Upon Completion"]
	removeblocks = options["Remove Blocks\\Entities Upon Completion (Stack or Combine mode only)"]
	find = options["Find\\Remove Variable:"]
	replace = options["Replace\\Add Variable:"]
	order = [orderx, ordery, orderz]
	orderdir = [0,0,0]
	for i in xrange(3):
		if order[i] == 0:
			orderdir[i] = xsort
		elif order[i] == 1:
			orderdir[i] = ysort
		elif order[i] == 2:
			orderdir[i] = zsort


	def ParseParams(spwn, listitem):
		if "sc" in listitem:
			if listitem["sc"][0] == "m":
				spwn["SpawnCount"] = TAG_Short(32767)
			else:
				spwn["SpawnCount"] = TAG_Short(toShort(int(listitem["sc"])))
		else:
			spwn["SpawnCount"] = TAG_Short(defnum)
		if "sr" in listitem:
			if listitem["sr"][0] == "m":
				spwn["SpawnRange"] = TAG_Short(32767)
			else:
				spwn["SpawnRange"] = TAG_Short(toShort(int(listitem["sr"])))
		else:
			spwn["SpawnRange"] = TAG_Short(defrange)
		if "me" in listitem:
			if listitem["me"][0] == "m":
				spwn["MaxNearbyEntities"] = TAG_Short(32767)
			else:
				spwn["MaxNearbyEntities"] = TAG_Short(toShort(int(listitem["me"])))
		else:
			spwn["MaxNearbyEntities"] = TAG_Short(defenties)
		if "pr" in listitem:
			if listitem["pr"][0] == "m":
				spwn["RequiredPlayerRange"] = TAG_Short(32767)
			else:
				spwn["RequiredPlayerRange"] = TAG_Short(toShort(int(listitem["pr"])))
		else:
			spwn["RequiredPlayerRange"] = TAG_Short(defradius)
		if "d" in listitem:
			if listitem["d"][0] == "m":
				spwn["Delay"] = TAG_Short(32767)
			else:
				spwn["Delay"] = TAG_Short(toShort(int(listitem["d"])))
		else:
			spwn["Delay"] = TAG_Short(defdelay)
			
		if "xd" in listitem:
			if listitem["xd"][0] == "m":
				spwn["MaxSpawnDelay"] = TAG_Short(32767)
			else:
				spwn["MaxSpawnDelay"] = TAG_Short(toShort(int(listitem["xd"])))
			if "md" not in listitem:
				spwn["MinSpawnDelay"] = TAG_Short(spwn["MaxSpawnDelay"].value)
			else:
				if listitem["md"][0] == "m":
					spwn["MinSpawnDelay"] = TAG_Short(32767)
				else:
					spwn["MinSpawnDelay"] = TAG_Short(toShort(int(listitem["md"])))
		else:
			if "md" in listitem:
				if listitem["md"][0] == "m":
					spwn["MinSpawnDelay"] = TAG_Short(32767)
					spwn["MaxSpawnDelay"] = TAG_Short(32767)
				else:
					spwn["MinSpawnDelay"] = TAG_Short(toShort(int(listitem["md"])))
					spwn["MaxSpawnDelay"] = TAG_Short(toShort(int(listitem["md"])))
			else:
				spwn["MaxSpawnDelay"] = TAG_Short(defmaxdelay)
				spwn["MinSpawnDelay"] = TAG_Short(defmindelay)

		if spwn["MinSpawnDelay"].value > spwn["MaxSpawnDelay"].value:
			spwn["MinSpawnDelay"] = TAG_Short(spwn["MaxSpawnDelay"].value)
			if spwn["MinSpawnDelay"].value <= 0:
				spwn["MinSpawnDelay"] = TAG_Short(1)
				spwn["MaxSpawnDelay"] = TAG_Short(1)

	def ParseDestParams(spwn, listitem):
		if "dsc" in listitem:
			if listitem["dsc"][0] == "m":
				spwn["SpawnCount"] = TAG_Short(32767)
			else:
				spwn["SpawnCount"] = TAG_Short(toShort(int(listitem["dsc"])))
		if "dsr" in listitem:
			if listitem["dsr"][0] == "m":
				spwn["SpawnRange"] = TAG_Short(32767)
			else:
				spwn["SpawnRange"] = TAG_Short(toShort(int(listitem["dsr"])))
		if "dme" in listitem:
			if listitem["dme"][0] == "m":
				spwn["MaxNearbyEntities"] = TAG_Short(32767)
			else:
				spwn["MaxNearbyEntities"] = TAG_Short(toShort(int(listitem["dme"])))
		if "dpr" in listitem:
			if listitem["dpr"][0] == "m":
				spwn["RequiredPlayerRange"] = TAG_Short(32767)
			else:
				spwn["RequiredPlayerRange"] = TAG_Short(toShort(int(listitem["dpr"])))
		if "dd" in listitem:
			if listitem["dd"][0] == "m":
				spwn["Delay"] = TAG_Short(32767)
			else:
				spwn["Delay"] = TAG_Short(toShort(int(listitem["dd"])))

		if "dxd" in listitem:
			if listitem["dxd"][0] == "m":
				spwn["MaxSpawnDelay"] = TAG_Short(32767)
			else:
				spwn["MaxSpawnDelay"] = TAG_Short(toShort(int(listitem["dxd"])))
			if "dmd" not in listitem:
				spwn["MinSpawnDelay"] = TAG_Short(spwn["MaxSpawnDelay"].value)
			else:
				if listitem["dmd"][0] == "m":
					spwn["MinSpawnDelay"] = TAG_Short(32767)
				else:
					spwn["MinSpawnDelay"] = TAG_Short(toShort(int(listitem["dmd"])))
		else:
			if "dmd" in listitem:
				if listitem["dmd"][0] == "m":
					spwn["MinSpawnDelay"] = TAG_Short(32767)
					spwn["MaxSpawnDelay"] = TAG_Short(32767)
				else:
					spwn["MinSpawnDelay"] = TAG_Short(toShort(int(listitem["dmd"])))
					spwn["MaxSpawnDelay"] = TAG_Short(toShort(int(listitem["dmd"])))

		if spwn["MinSpawnDelay"].value > spwn["MaxSpawnDelay"].value:
			spwn["MinSpawnDelay"] = TAG_Short(spwn["MaxSpawnDelay"].value)
			if spwn["MinSpawnDelay"].value <= 0:
				spwn["MinSpawnDelay"] = TAG_Short(1)
				spwn["MaxSpawnDelay"] = TAG_Short(1)
				
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

	def CreatePlaceholder(px,py,pz):
		place = deepcopy(cart)
		place["RequiredPlayerRange"] = TAG_Short(0)
		place["SpawnData"]["Pos"][1] = TAG_Double(-1.0)
		place["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(0.0)
		place["OnGround"] = TAG_Byte(1)
		place["Motion"] = TAG_List()
		place["Motion"].append(TAG_Double(0.0))
		place["Motion"].append(TAG_Double(0.0))
		place["Motion"].append(TAG_Double(0.0))
		place["Pos"][0] = TAG_Double(px)
		place["Pos"][1] = TAG_Double(py)
		place["Pos"][2] = TAG_Double(pz)
		px = int(px)
		pz = int(pz)
		chnk = level.getChunk(px>>4,pz>>4)
		chnk.Entities.append(place)


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
	commandblock = False
	
	for src in sources:
		cartlist = []

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
		spawner = TAG_Compound()
		spawner["x"] = TAG_Int(x+srcx)
		spawner["y"] = TAG_Int(y+srcy)
		spawner["z"] = TAG_Int(z+srcz)
		spawner["id"] = TAG_String("MobSpawner")

		cart = TAG_Compound()
		cart["id"] = TAG_String("MinecartSpawner")
		cart["Rotation"] = TAG_List()
		cart["Rotation"].append(TAG_Float(0.0))
		cart["Rotation"].append(TAG_Float(0.0))
		
		ParseParams(spawner, src)

		cart["Pos"] = TAG_List()
		
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
			cart["Pos"].append(TAG_Double(cx))
			cart["Pos"].append(TAG_Double(cy))
			cart["Pos"].append(TAG_Double(cz))
			if "sr" in src["midwayobj"]:
				spawner["SpawnRange"] = TAG_Short(toShort(int(src["midwayobj"]["sr"])))
			else:
				if "comb" in src["midwayobj"] or "multi" in src["midwayobj"] or "stack" in src["midwayobj"] or "seth" in src["midwayobj"]:
					spawner["SpawnRange"] = TAG_Short(defrange)
				else:
					dx = x - src["midwayobj"]["obj"]["x"].value
					dz = z - src["midwayobj"]["obj"]["z"].value
					my = src["midwayobj"]["obj"]["y"].value
					if my > (y+srcy):
						if (my - (y+srcy)) > 4:
							print "ERROR! Midway sign",src["midwayobj"]["id"],"is too far above source sign",src["id"],"!"
							continue
					else:
						if ((y+srcy) - my) > 4:					
							print "ERROR! Midway sign",src["midwayobj"]["id"],"is too far below source sign",src["id"],"!"
							continue
					spawner["SpawnRange"] = TAG_Short(toShort(max(abs(dx),abs(dz))))
			if "comb" in src["midwayobj"] or "multi" in src["midwayobj"] or "stack" in src["midwayobj"] or "seth" in src["midwayobj"]:
				spawner["MaxNearbyEntities"] = TAG_Short(defenties)
			else:
				spawner["MaxNearbyEntities"] = TAG_Short(toShort(src["midwayobj"]["count"]))
		else:
			cx = x+0.5
			cy = y+0.5
			cz = z+0.5
			if "x" in src:
				cx += float(src["x"])
			if "y" in src:
				cy += float(src["y"])
			if "z" in src:
				cz += float(src["z"])
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
				ent = deepcopy(ents[0])
			if "UUIDMost" in ent:
				del ent["UUIDMost"]
			if "UUIDLeast" in ent:
				del ent["UUIDLeast"]
			dests = FindID(src["id"])
			if dests == None:
				print "Error! No matching destination sign found within selection for sign at", x, y, z
				continue
			for dest in dests:
				spawner["EntityId"] = TAG_String("MinecartSpawner")
				cart["EntityId"] = TAG_String(ent["id"].value)
				cart["SpawnData"] = TAG_Compound()
				cart["SpawnData"] = deepcopy(ent)
				sx = dest["obj"]["x"].value+0.5
				sy = dest["obj"]["y"].value+0.5
				sz = dest["obj"]["z"].value+0.5
				ParseParams(cart,dest)
				ParseDestParams(cart,src)
				ParseInnerParams(cart,src)
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
				cart["SpawnPotentials"] = TAG_List()
				pot = TAG_Compound()
				pot["Type"] = TAG_String(cart["EntityId"].value)
				pot["Weight"] = TAG_Int(1)
				pot["Properties"] = deepcopy(cart["SpawnData"])
				cart["SpawnPotentials"].append(pot)
				if "multi" not in dest and "dmulti" not in src:
					if tileent:
						cart["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(-50.0)
					else:
						cart["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(0)
					if "md" not in dest and "xd" not in dest and "dmd" not in src and "dxd" not in src:
						cart["MinSpawnDelay"] = TAG_Short(32767)
						cart["MaxSpawnDelay"] = TAG_Short(32767)
				if "multi" in dest or "dmulti" in src:
					cart["SpawnData"]["Pos"][1] = TAG_Double(-1)
					cart["SpawnData"]["Time"] = TAG_Byte(-100)

				dest["CanDelete"] = True
				weight = toInt(int(src["dwt"] if "dwt" in src else dest["wt"] if "wt" in dest else 1))
				cartlist.append((deepcopy(cart),weight))

			spawner["SpawnData"] = deepcopy(cart)
			spawner["SpawnPotentials"] = TAG_List()
			for ct, wt in cartlist:
				pot2 = TAG_Compound()
				pot2["Type"] = TAG_String(spawner["EntityId"].value)
				pot2["Weight"] = TAG_Int(wt)
				pot2["Properties"] = deepcopy(ct)
				spawner["SpawnPotentials"].append(pot2)
				
			chnk = level.getChunk(x>>4,z>>4)

			if "cmd" in src:
				commandblock = True
			else:
				commandblock = False
			
			combstack = False
			if "midwayobj" in src and not commandblock:
				if "comb" in src["midwayobj"] or "multi" in src["midwayobj"] or "stack" in src["midwayobj"] or "seth" in src["midwayobj"]:
					combstack = True
			
			if combstack:
				idval = src["midwayobj"]["id"]
				if idval not in spawnerlist:
					spawnerlist[idval] = {}
					spawnerlist[idval]["master"] = src["midwayobj"]
					spawnerlist[idval]["spawners"] = []
				if "%smain" in src:
					spawnerlist[idval]["mainsign"] = src
				weight = src["wt"] if "wt" in src else 1
				for ct, wt in cartlist:
					spawnerlist[idval]["spawners"].append({"weight":wt,"cart":ct})
				
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
				bx = spawner["x"].value
				by = spawner["y"].value
				bz = spawner["z"].value
				if "cmd" in src:
					chnk.TileEntities.append(CreateCommandBlock(bx,by,bz,spawner["SpawnData"]["SpawnData"],spawner["SpawnData"]["EntityId"].value))
					level.setBlockAt(bx, by, bz, 137)
					level.setBlockDataAt(bx, by, bz, 0)
				else:
					chnk.TileEntities.append(spawner)
					level.setBlockAt(bx, by, bz, 52)
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
			dests = FindID(src["id"])
			if dests == None:
				print "Error! No matching destination sign found within selection for sign at", x, y, z
				continue
			for dest in dests:
				spawner["EntityId"] = TAG_String("MinecartSpawner")
				cart["EntityId"] = TAG_String("FallingSand")
				cart["SpawnData"] = TAG_Compound()
				cart["SpawnData"]["TileID"] = TAG_Int(block)
				cart["SpawnData"]["Data"] = TAG_Byte(data)
				if tent != None:
					cart["SpawnData"]["TileEntityData"] = deepcopy(tent)
				sx = dest["obj"]["x"].value+0.5
				sy = dest["obj"]["y"].value+0.5
				sz = dest["obj"]["z"].value+0.5
				ParseParams(cart,dest)
				ParseDestParams(cart,src)
				ParseInnerParams(cart,src)
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

				cart["SpawnPotentials"] = TAG_List()
				pot = TAG_Compound()
				pot["Type"] = TAG_String(cart["EntityId"].value)
				pot["Weight"] = TAG_Int(1)
				pot["Properties"] = deepcopy(cart["SpawnData"])
				cart["SpawnPotentials"].append(pot)
				if "multi" not in dest and "dmulti" not in src:
					cart["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(-1.0)
					cart["SpawnPotentials"][0]["Properties"]["Time"] = TAG_Byte(100)
					if "md" not in dest and "xd" not in dest and "dmd" not in src and "dxd" not in src:
						cart["MinSpawnDelay"] = TAG_Short(32767)
						cart["MaxSpawnDelay"] = TAG_Short(32767)
				if "multi" in dest or "dmulti" in src:
					cart["SpawnData"]["Pos"][1] = TAG_Double(-1)
					cart["SpawnData"]["Time"] = TAG_Byte(-100)

				dest["CanDelete"] = True
				weight = toInt(int(src["dwt"] if "dwt" in src else dest["wt"] if "wt" in dest else 1))
				cartlist.append((deepcopy(cart),weight))
				
			spawner["SpawnData"] = deepcopy(cart)
			spawner["SpawnPotentials"] = TAG_List()
			for ct, wt in cartlist:
				pot2 = TAG_Compound()
				pot2["Type"] = TAG_String(spawner["EntityId"].value)
				pot2["Weight"] = TAG_Int(wt)
				pot2["Properties"] = deepcopy(ct)
				spawner["SpawnPotentials"].append(pot2)

			chnk = level.getChunk(x>>4,z>>4)
			
			if "cmd" in src:
				commandblock = True
			else:
				commandblock = False
			
			combstack = False
			if "midwayobj" in src and not commandblock:
				if "comb" in src["midwayobj"] or "multi" in src["midwayobj"] or "stack" in src["midwayobj"] or "seth" in src["midwayobj"]:
					combstack = True

			if combstack:
				idval = src["midwayobj"]["id"]
				if idval not in spawnerlist:
					spawnerlist[idval] = {}
					spawnerlist[idval]["master"] = src["midwayobj"]
					spawnerlist[idval]["spawners"] = []
				if "%smain" in src:
					spawnerlist[idval]["mainsign"] = src

				for ct, wt in cartlist:
					spawnerlist[idval]["spawners"].append({"weight":wt,"cart":ct})
				if removeblocks:
					if tent != None:
						chnk.TileEntities.remove(tent)
					level.setBlockAt(x+srcx, y+srcy, z+srcz, 0)
					level.setBlockDataAt(x+srcx, y+srcy, z+srcz, 0)
			else:
				if tent != None:
					chnk.TileEntities.remove(tent)

				bx = spawner["x"].value
				by = spawner["y"].value
				bz = spawner["z"].value
				if "cmd" in src:
					chnk.TileEntities.append(CreateCommandBlock(bx,by,bz,spawner["SpawnData"]["SpawnData"],spawner["SpawnData"]["EntityId"].value))
					level.setBlockAt(bx, by, bz, 137)
					level.setBlockDataAt(bx, by, bz, 0)
				else:
					chnk.TileEntities.append(spawner)
					level.setBlockAt(bx, by, bz, 52)
					level.setBlockDataAt(bx, by, bz, 0)
				chnk.dirty = True
			src["CanDelete"] = True
			if "midwayobj" in src:
				src["midwayobj"]["CanDelete"] = True
	
		if placeholder and not combstack and not commandblock:
			CreatePlaceholder(cart["Pos"][0].value,cart["Pos"][1].value,cart["Pos"][2].value)

	if not commandblock:
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
			spawner = TAG_Compound()
			spawner["x"] = TAG_Int(x)
			spawner["y"] = TAG_Int(y)
			spawner["z"] = TAG_Int(z)
			spawner["id"] = TAG_String("MobSpawner")
			ParseParams(spawner, spawnerlist[key]["master"])
			spawner["EntityId"] = TAG_String("MinecartSpawner")
			if "stack" in spawnerlist[key]["master"]:
				riding = None
				for pair in spawnerlist[key]["spawners"]:
					if "SpawnData" not in spawner:
						spawner["SpawnData"] = deepcopy(pair["cart"])
						if ox != None:
							spawner["SpawnData"]["Pos"][0] = TAG_Double(ox)
						if oy != None:
							spawner["SpawnData"]["Pos"][1] = TAG_Double(oy)
						if oz != None:
							spawner["SpawnData"]["Pos"][2] = TAG_Double(oz)
						spawner["SpawnData"]["Riding"] = TAG_Compound()
						riding = spawner["SpawnData"]
					riding["Riding"] = deepcopy(pair["cart"])
					riding = riding["Riding"]
				if "SpawnPotentials" not in spawner:
					spawner["SpawnPotentials"] = TAG_List()
				spawner["SpawnPotentials"].append(TAG_Compound())
				spawner["SpawnPotentials"][-1]["Type"] = TAG_String("MinecartSpawner")
				spawner["SpawnPotentials"][-1]["Weight"] = TAG_Int(1)
				spawner["SpawnPotentials"][-1]["Properties"] = deepcopy(spawner["SpawnData"])
			elif "comb" in spawnerlist[key]["master"]:
				if "SpawnPotentials" not in spawner:
					spawner["SpawnPotentials"] = TAG_List()
				for pair in spawnerlist[key]["spawners"]:
					pot = TAG_Compound()
					pot["Weight"] = TAG_Int(pair["weight"])
					pot["Type"] = TAG_String("MinecartSpawner")
					pot["Properties"] = deepcopy(pair["cart"])
					if ox != None:
						pot["Properties"]["Pos"][0] = TAG_Double(ox)
					if oy != None:
						pot["Properties"]["Pos"][1] = TAG_Double(oy)
					if oz != None:
						pot["Properties"]["Pos"][2] = TAG_Double(oz)
					spawner["SpawnPotentials"].append(pot)
				pot = random.choice(spawner["SpawnPotentials"])
				spawner["SpawnData"] = deepcopy(pot["Properties"])
				spawner["SpawnData"]["EntityId"] = TAG_String(pot["Type"].value)
			elif "multi" in spawnerlist[key]["master"]:
				crt = None
				for pair in spawnerlist[key]["spawners"]:
					if crt == None:
						crt = deepcopy(pair["cart"])
						del crt["SpawnPotentials"]
						crt["SpawnPotentials"] = TAG_List()
					pot = TAG_Compound()
					pot["Weight"] = TAG_Int(pair["weight"])
					pot["Type"] = TAG_String(pair["cart"]["EntityId"].value)
					pot["Properties"] = deepcopy(pair["cart"]["SpawnData"])
					crt["SpawnPotentials"].append(pot)
				
				pot = random.choice(crt["SpawnPotentials"])
				if ox != None:
					crt["Pos"][0] = TAG_Double(ox)
				if oy != None:
					crt["Pos"][1] = TAG_Double(oy)
				if oz != None:
					crt["Pos"][2] = TAG_Double(oz)
				crt["SpawnData"] = deepcopy(pot["Properties"])
				crt["SpawnData"]["Pos"][1] = TAG_Double(-1)
				crt["SpawnData"]["Time"] = TAG_Byte(100)
				spawner["SpawnData"] = deepcopy(crt)
				spawner["SpawnData"]["EntityId"] = TAG_String(pot["Type"].value)
				ParseParams(spawner["SpawnData"], spawnerlist[key]["master"])
				spawner["SpawnData"]["Delay"] = TAG_Short(5)
				ParseDestParams(spawner["SpawnData"],spawnerlist[key]["master"])
				if "SpawnPotentials" not in spawner:
					spawner["SpawnPotentials"] = TAG_List()
				spawner["SpawnPotentials"].append(TAG_Compound())
				spawner["SpawnPotentials"][-1]["Type"] = TAG_String("MinecartSpawner")
				spawner["SpawnPotentials"][-1]["Weight"] = TAG_Int(1)
				spawner["SpawnPotentials"][-1]["Properties"] = deepcopy(spawner["SpawnData"])
			elif "seth" in spawnerlist[key]["master"]:
				if spawnerlist[key]["master"]["seth"] != "" and spawnerlist[key]["master"]["seth"] != "rand":
					orderstr = spawnerlist[key]["master"]["seth"]
					orderstr = orderstr.replace("-","")
					for i in xrange(3):
						if orderstr[i] == "x":
							order[i] = 0
							if "-x" in spawnerlist[key]["master"]["seth"]:
								orderdir[i] = -1
							else:
								orderdir[i] = 1
						elif orderstr[i] == "y":
							order[i] = 1
							if "-y" in spawnerlist[key]["master"]["seth"]:
								orderdir[i] = -1
							else:
								orderdir[i] = 1
						elif orderstr[i] == "z":
							order[i] = 2
							if "-z" in spawnerlist[key]["master"]["seth"]:
								orderdir[i] = -1
							else:
								orderdir[i] = 1
				if spawnerlist[key]["master"]["seth"] == "rand":
					random.shuffle(spawnerlist[key]["spawners"])
				else:
					spawnerlist[key]["spawners"].sort(key=lambda s: (s["cart"]["SpawnData"]["Pos"][order[0]].value * orderdir[0], s["cart"]["SpawnData"]["Pos"][order[1]].value * orderdir[1], s["cart"]["SpawnData"]["Pos"][order[2]].value * orderdir[2]))

				sx = float(x)+0.5
				sy = float(y)-0.5
				sz = float(z)+0.5
				spawner["SpawnData"] = TAG_Compound()
				spawner["SpawnData"]["Pos"] = TAG_List()
				spawner["SpawnData"]["Pos"].append(TAG_Double(x+0.5))
				spawner["SpawnData"]["Pos"].append(TAG_Double(y+1.5))
				spawner["SpawnData"]["Pos"].append(TAG_Double(z+0.5))
				spawner["SpawnData"]["Rotation"] = TAG_List()
				spawner["SpawnData"]["Rotation"].append(TAG_Float(0.0))
				spawner["SpawnData"]["Rotation"].append(TAG_Float(0.0))
				spawner["SpawnData"]["id"] = TAG_String("MinecartSpawner")
				spawner["SpawnData"]["EntityId"] = TAG_String("MinecartSpawner")
				spawner["SpawnData"]["SpawnRange"] = TAG_Short(0)
				spawner["SpawnData"]["SpawnCount"] = TAG_Short(1)
				spawner["SpawnData"]["Delay"] = TAG_Short(10)
				spawner["SpawnData"]["MinSpawnDelay"] = TAG_Short(32767)
				spawner["SpawnData"]["MaxSpawnDelay"] = TAG_Short(32767)
				spawner["SpawnData"]["MaxNearbyEntities"] = TAG_Short(2)
				spawner["SpawnData"]["RequiredPlayerRange"] = TAG_Short(toShort(int(spawnerlist[key]["master"]["pr"])) if "pr" in spawnerlist[key]["master"] else defradius)
				dummy = deepcopy(spawner["SpawnData"])
				dummy["Pos"][0] = TAG_Double(sx)
				dummy["Pos"][1] = TAG_Double(sy)
				dummy["Pos"][2] = TAG_Double(sz)
				dummy["EntityId"] = TAG_String("XPOrb")
				dummy["RequiredPlayerRange"] = TAG_Short(0)
				dummy["Delay"] = TAG_Short(32767)
				spawner["SpawnData"]["SpawnPotentials"] = TAG_List()
				spawner["SpawnData"]["SpawnPotentials"].append(TAG_Compound())
				spawner["SpawnData"]["SpawnPotentials"][0]["Type"] = TAG_String("MinecartSpawner")
				spawner["SpawnData"]["SpawnPotentials"][0]["Weight"] = TAG_Int(1)
				spawner["SpawnData"]["SpawnPotentials"][0]["Properties"] = deepcopy(dummy)

				first = True
				for pair in spawnerlist[key]["spawners"]:
					if first:
						spawner["SpawnData"]["SpawnData"] = deepcopy(pair["cart"])
						blah = spawner["SpawnData"]["SpawnData"]
						first = False
					else:
						blah["SpawnPotentials"] = TAG_List()
						blah["SpawnPotentials"].append(TAG_Compound())
						blah["SpawnPotentials"][0]["Type"] = TAG_String("MinecartSpawner")
						blah["SpawnPotentials"][0]["Weight"] = TAG_Int(1)
						blah["SpawnPotentials"][0]["Properties"] = deepcopy(pair["cart"])
						blah = blah["SpawnPotentials"][0]["Properties"]
					blah["MaxNearbyEntities"] = TAG_Short(32767)
					blah["Pos"][0] = TAG_Double(sx)
					blah["Pos"][1] = TAG_Double(sy)
					blah["Pos"][2] = TAG_Double(sz)
					blah["SpawnRange"] = TAG_Short(0)
					blah["Delay"] = TAG_Short(0)
					blah["MinSpawnDelay"] = TAG_Short(2)
					blah["MaxSpawnDelay"] = TAG_Short(2)
				else:
					blah["SpawnPotentials"] = TAG_List()
					blah["SpawnPotentials"].append(TAG_Compound())
					blah["SpawnPotentials"][0]["Type"] = TAG_String("MinecartSpawner")
					blah["SpawnPotentials"][0]["Weight"] = TAG_Int(1)
					blah["SpawnPotentials"][0]["Properties"] = deepcopy(dummy)
				if "SpawnPotentials" in spawner:
					del spawner["SpawnPotentials"]
			else:
				print "ERROR! Filter incorrectly processed an item!  No stack or comb in stacking and combing area!"
				continue

			CreatePlaceholder(spawner["SpawnData"]["Pos"][0].value,spawner["SpawnData"]["Pos"][1].value,spawner["SpawnData"]["Pos"][2].value)
			chnk = level.getChunk(x>>4,z>>4)
			chnk.TileEntities.append(spawner)
			level.setBlockAt(x, y, z, 52)
			level.setBlockDataAt(x, y, z, 0)
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