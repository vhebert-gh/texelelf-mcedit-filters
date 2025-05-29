from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float, TAG_Long, TAG_Byte_Array, TAG_Int_Array
from copy import deepcopy

displayName = "Chest Contents to Command Block"
inputs = (
	("Command Block Type:",("Command Blocks","Minecart Command Blocks")),
	("Command Type:",("Summon","Give","Clear","Testfor","Scoreboard players...")),
	("Command Block Name:",("string","value=@")),
	("Target (All Commands Except Summon):",("string","value=@a")),
	("Scoreboard players...",("set","add","remove")),
	("Scoreboard players objective name:",("string","value=ObjectiveName")),
	("Scoreboard players score amount:",(0,-2147483648,2147483648)),
	("Remove slot tag:",True),
	("Remove damage tag:",False),
	("Remove count tag:",False),
	("Number of items to clear:",(0,0,32767)),
	("Summon-only options:","label"),
	("Item does not despawn:",False),
	("Item cannot be picked up:",False),
	("Below Coordinates are Relative to Command Block:",True),
	("X Summon Position:",0.0),
	("Y Summon Position:",0.0),
	("Z Summon Position:",0.0),
	)

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
	command = options["Command Type:"]
	comname = options["Command Block Name:"]
	target = options["Target (All Commands Except Summon):"]
	scoretype = options["Scoreboard players..."]
	scorename = options["Scoreboard players objective name:"]
	scoreamount = options["Scoreboard players score amount:"]
	removeslot  = options["Remove slot tag:"]
	removedamage = options["Remove damage tag:"]
	removecount = options["Remove count tag:"]
	numclear = options["Number of items to clear:"]
	donotdespawn = options["Item does not despawn:"]
	nopickup = options["Item cannot be picked up:"]
	relative = options["Below Coordinates are Relative to Command Block:"]
	posx = options["X Summon Position:"]
	posy = options["Y Summon Position:"]
	posz = options["Z Summon Position:"]
	
	if "@e" in target:
		if "!Player" in target:
			InventoryTest = False
		elif "Player" in target:
			InventoryTest = True
		else:
			InventoryTest = False
	else:
		InventoryTest = True
	
	entsToAdd = []
	entsToDelete = []
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:
				if e["id"].value != "Chest":
					continue
				if "Items" not in e:
					continue
				if len(e["Items"]) <= 0:
					continue

				ent = TAG_Compound()
				if len(e["Items"]) == 1:
					type = "Item"
					if command == "Give" or command == "Clear" or command == "Summon":
						ent["Item"] = deepcopy(e["Items"][0])
						entptr = ent["Item"]

						if command == "Summon":
							if donotdespawn:
								ent["Age"] = TAG_Short(-32768)
							if nopickup :
								ent["PickupDelay"] = TAG_Short(32767)
					else:
						if InventoryTest:
							ent["Inventory"] = deepcopy(e["Items"])
							entptr = ent["Inventory"][0]
						else:
							ent["Equipment"] = deepcopy(e["Items"])
							entptr = ent["Equipment"][0]

					if "Slot" in entptr and (command == "Summon" or removeslot):
						del entptr["Slot"]

					if command != "Give" and command != "Clear":
						if "Damage" in entptr and removedamage:
							del entptr["Damage"]
						if "Count" in entptr and removecount:
							del entptr["Count"]
				else:
					if command == "Give" or command == "Clear":
						continue
					elif command == "Summon":
						type = "Item"
						entptr = ent
						for item in e["Items"]:
							entptr["Item"] = deepcopy(item)
							entptr["id"] = TAG_String("Item")
							if "Slot" in entptr["Item"]:
								del entptr["Item"]["Slot"]
							if donotdespawn:
								entptr["Age"] = TAG_Short(-32768)
							if nopickup :
								entptr["PickupDelay"] = TAG_Short(32767)
							entptr["Riding"] = TAG_Compound()
							entptr = entptr["Riding"]
					else:
						if InventoryTest:
							ent["Inventory"] = deepcopy(e["Items"])
							entptr = ent["Inventory"]
						else:
							ent["Equipment"] = deepcopy(e["Items"])
							entptr = ent["Equipment"]

						for item in entptr:
							if "Slot" in item and removeslot:
								del item["Slot"]
							if "Damage" in item and removedamage:
								del item["Damage"]
							if "Count" in item and removecount:
								del item["Count"]

						
				if relative:
					sx = "~" + (str(posx) if posx != 0.0 else "")
					sy = "~" + (str(posy) if posy != 0.0 else "")
					sz = "~" + (str(posz) if posz != 0.0 else "")
				else:
					sx = str(posx)
					sy = str(posy)
					sz = str(posz)
							
				newcommand = TAG_Compound()

				if command == "Summon":
					spawndata = "{"+NBT2Command(ent)+"}"
					commandstr = TAG_String(unicode("summon {} {} {} {} {}".format(unicode(type), unicode(sx), unicode(sy), unicode(sz), unicode(spawndata)).decode("unicode-escape")))
				else:
					if "Item" in ent:
						id = ent["Item"]["id"].value
						damage = str(ent["Item"]["Damage"].value)
						count = str(ent["Item"]["Count"].value)
						if "tag" in ent["Item"]:
							meta = "{"+NBT2Command(ent["Item"]["tag"])+"}"
						else:
							meta = ""
					else:
						meta = "{"+NBT2Command(ent)+"}"
					if command == "Give":
						commandstr = TAG_String(unicode("give {} {} {} {} {}".format(unicode(target), unicode(id), unicode(count), unicode(damage), unicode(meta)).decode("unicode-escape")))				
					elif command == "Clear":
						commandstr = TAG_String(unicode("clear {} {} {} {} {}".format(unicode(target), unicode(id), unicode(damage), unicode(numclear), unicode(meta)).decode("unicode-escape")))				
					elif command == "Testfor":
						commandstr = TAG_String(unicode("testfor {} {}".format(unicode(target), unicode(meta)).decode("unicode-escape")))				
					elif command == "Scoreboard players...":
						commandstr = TAG_String(unicode("scoreboard players {} {} {} {} {}".format(unicode(scoretype), unicode(target), unicode(scorename), unicode(scoreamount), unicode(meta)).decode("unicode-escape")))				

				if blocktype == "Command Blocks":
					newcommand["id"] = TAG_String("Control")
					newcommand["x"] = TAG_Int(x)
					newcommand["y"] = TAG_Int(y)
					newcommand["z"] = TAG_Int(z)
					newcommand["CustomName"] = TAG_String(comname)
					newcommand["TrackOutput"] = TAG_Byte(0)
					level.setBlockAt(x, y, z, 137)
					level.setBlockDataAt(x, y, z, 0)
				else:
					newcommand["id"] = TAG_String("MinecartCommandBlock")
					newcommand["Fire"] = TAG_Short(-1)
					newcommand["OnGround"] = TAG_Byte(0)
					newcommand["FallDistance"] = TAG_Float(0.0)
					newcommand["Rotation"] = TAG_List([TAG_Float(0.0),TAG_Float(0.0)])
					newcommand["Motion"] = TAG_List([TAG_Double(0.0),TAG_Double(0.0),TAG_Double(0.0)])
					newcommand["CustomName"] = TAG_String(comname)
					newcommand["TrackOutput"] = TAG_Byte(0)
					newcommand["Pos"] = TAG_List([TAG_Double(float(x)+0.5),TAG_Double(float(y)+0.5),TAG_Double(float(z)+0.5)])
					level.setBlockAt(x, y, z, 0)
					level.setBlockDataAt(x, y, z, 0)
				newcommand["Command"] = commandstr
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


