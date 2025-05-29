from copy import deepcopy
from pymclevel import TAG_String, TAG_Compound, TAG_List, TAG_Byte, TAG_Short
from pymclevel import TileEntity

displayName = "SirVladimyr's Locksmith Filter"

sectional = "\xA7"

inputs = (
	("Create Hopper",False),
	("Key Item ID:",(0,-32768,32767)),
	("Key Item Damage",(0,-32768,32767)),
	("Number of Keys",(42,1,32767)),
	("Sectional stand-in character",("string","value=|","width=30")),
	("Name:",("string","value=")),
	("Lore 1:",("string","value=")),
	("Lore 2:",("string","value=")),
	("Lore 3:",("string","value=")),
	)

def perform(level, box, options):
	create = options["Create Hopper"]
	id = options["Key Item ID:"]
	if id == 0:
		print "ERROR! Invalid ID number!"
		return
	damage = options["Key Item Damage"]
	numitems = options["Number of Keys"]
		
	standinchar = options["Sectional stand-in character"]
	if options["Name:"] != "":
		name = options["Name:"].encode("unicode-escape")
		name = name.replace(str(standinchar),sectional)
		name = name.decode("unicode-escape")
	else:
		name = ""
	
	lore = []
	if options["Lore 1:"] != "":
		temp = options["Lore 1:"].encode("unicode-escape")
		temp = temp.replace(str(standinchar),sectional)
		temp = temp.decode("unicode-escape")
		lore.append(temp)
	if options["Lore 2:"] != "":
		temp = options["Lore 2:"].encode("unicode-escape")
		temp = temp.replace(str(standinchar),sectional)
		temp = temp.decode("unicode-escape")
		lore.append(temp)
	if options["Lore 3:"] != "":
		temp = options["Lore 3:"].encode("unicode-escape")
		temp = temp.replace(str(standinchar),sectional)
		temp = temp.decode("unicode-escape")
		lore.append(temp)
		
	for (chunk, slices, point) in level.getChunkSlices(box):
		if create:
			(cx,cz) = chunk.chunkPosition
			cposx = cx * 16
			cposz = cz * 16
			for y in range(box.miny,box.maxy,1):
				for x in range((cposx if (cposx > box.minx) else box.minx),(cposx+16 if ((cposx+16) < box.maxx) else box.maxx),1):
					for z in range((cposz if (cposz > box.minz) else box.minz),(cposz+16 if((cposz+16) < box.maxz) else box.maxz),1):
						level.setBlockAt(x, y, z, 154)
						e = TileEntity.Create("Hopper")
						TileEntity.setpos(e, (x, y, z))
						chunk.TileEntities.append(e)
			chunk.dirty = True

		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if e["id"].value == "Hopper":
					if "Items" in e:
						del e["Items"]
					e["Items"] = TAG_List()
					numslots = 5

					place = numitems / numslots
					remainder = numitems % numslots
					if place < 1:
						place = remainder
						remainder = 0
						numslots = 1
					elif place >= 64:
						place = 64
						remainder = 0
					item = TAG_Compound()
					item["id"] = TAG_Short(id)
					item["Damage"] = TAG_Short(damage)
					item["Count"] = TAG_Byte(place)
					if name != "" or len(lore) > 0:
						item["tag"] = TAG_Compound()
						item["tag"]["display"] = TAG_Compound()
						if name != "":
							item["tag"]["display"]["Name"] = TAG_String(name)
						if len(lore) > 0:
							item["tag"]["display"]["Lore"] = TAG_List()
							for i in xrange(0,len(lore)):
								item["tag"]["display"]["Lore"].append(TAG_String(lore[i]))
					for i in range(0,numslots):
						itemcopy = deepcopy(item)
						itemcopy["Slot"] = TAG_Byte(i)
						e["Items"].append(itemcopy)
						del itemcopy
					else:
						e["Items"][i]["Count"] = TAG_Byte(e["Items"][i]["Count"].value + remainder)
						
					chunk.dirty = True
