from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Float
from pymclevel import TAG_Double
from pymclevel import TAG_String

displayName = "Set Equipment on Mobs and Spawners"

inputs = (
	("This label serves no other purpose than to force the filter to be displayed two-columns wide.","label"),
	("Apply to:", ("Entities","Spawners")),
	("Hand Item ID",0),
	("Hand Item Damage",0),
	("Hand Item Count",1),
	("Hand Item Drop Percent",5.0),
	("Helmet Item ID",0),
	("Helmet Item Damage",0),
	("Helmet Item Count",1),
	("Helmet Item Drop Percent",5.0),
	("Chest Item ID",0),
	("Chest Item Damage",0),
	("Chest Item Count",1),
	("Chest Item Drop Percent",5.0),
	("Leggings Item ID",0),
	("Leggings Item Damage",0),
	("Leggings Item Count",1),
	("Leggings Item Drop Percent",5.0),
	("Feet Item ID",0),
	("Feet Item Damage",0),
	("Feet Item Count",1),
	("Feet Item Drop Percent",5.0),
	)

def perform(level, box, options):
	applytype = options["Apply to:"]
	
	handid = options["Hand Item ID"]
	handdamage = options["Hand Item Damage"]
	handcount = options["Hand Item Count"]
	handdrop = options["Hand Item Drop Percent"]
	
	helmetid = options["Helmet Item ID"]
	helmetdamage = options["Helmet Item Damage"]
	helmetcount = options["Helmet Item Count"]
	helmetdrop = options["Helmet Item Drop Percent"]

	chestid = options["Chest Item ID"]
	chestdamage = options["Chest Item Damage"]
	chestcount = options["Chest Item Count"]
	chestdrop = options["Chest Item Drop Percent"]

	leggingid = options["Leggings Item ID"]
	leggingdamage = options["Leggings Item Damage"]
	leggingcount = options["Leggings Item Count"]
	leggingdrop = options["Leggings Item Drop Percent"]

	feetid = options["Feet Item ID"]
	feetdamage = options["Feet Item Damage"]
	feetcount = options["Feet Item Count"]
	feetdrop = options["Feet Item Drop Percent"]

	handitem = TAG_Compound()
	if handid != 0:
		handitem["id"] = TAG_Short(handid)
		handitem["Damage"] = TAG_Short(handdamage)
		handitem["Count"] = TAG_Byte(handcount)

	helmetitem = TAG_Compound()
	if helmetid != 0:
		helmetitem["id"] = TAG_Short(helmetid)
		helmetitem["Damage"] = TAG_Short(helmetdamage)
		helmetitem["Count"] = TAG_Byte(helmetcount)		

	chestitem = TAG_Compound()
	if chestid != 0:
		chestitem["id"] = TAG_Short(chestid)
		chestitem["Damage"] = TAG_Short(chestdamage)
		chestitem["Count"] = TAG_Byte(chestcount)

	leggingitem = TAG_Compound()
	if leggingid != 0:
		leggingitem["id"] = TAG_Short(leggingid)
		leggingitem["Damage"] = TAG_Short(leggingdamage)
		leggingitem["Count"] = TAG_Byte(leggingcount)

	feetitem = TAG_Compound()
	if feetid != 0:
		feetitem["id"] = TAG_Short(feetid)
		feetitem["Damage"] = TAG_Short(feetdamage)
		feetitem["Count"] = TAG_Byte(feetcount)		

	handdrop = TAG_Float((handdrop * .01) if handdrop != 5.0 else 0.05000000074505806)
	helmetdrop = TAG_Float((helmetdrop * .01) if helmetdrop != 5.0 else 0.05000000074505806)
	chestdrop = TAG_Float((chestdrop * .01) if chestdrop != 5.0 else 0.05000000074505806)
	leggingdrop = TAG_Float((leggingdrop * .01) if leggingdrop != 5.0 else 0.05000000074505806)
	feetdrop = TAG_Float((feetdrop * .01) if feetdrop != 5.0 else 0.05000000074505806)

	droplist = TAG_List()
	droplist.append(handdrop)
	droplist.append(feetdrop)
	droplist.append(leggingdrop)
	droplist.append(chestdrop)
	droplist.append(helmetdrop)
		
	for (chunk, slices, point) in level.getChunkSlices(box):
		if applytype == "Entities":
			for e in chunk.Entities:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
				
				if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
					if "Health" in e:
						if "Equipment" in e:
							del e["Equipment"]
						e["Equipment"] = TAG_List()
						e["Equipment"].append(handitem)
						e["Equipment"].append(feetitem)						
						e["Equipment"].append(leggingitem)
						e["Equipment"].append(chestitem)
						e["Equipment"].append(helmetitem)
						
						if "DropChances" in e:
							del e["DropChances"]
						e["DropChances"] = TAG_List(droplist)
						
						chunk.dirty = True

		else:
			for e in chunk.TileEntities:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
					if e["id"].value == "MobSpawner":
						if "SpawnData" not in e:
							e["SpawnData"] = TAG_Compound()
							e["SpawnData"]["EntityId"] = e["EntityId"]
						else:
							if "Equipment" in e["SpawnData"]:
								del e["SpawnData"]["Equipment"]

						e["SpawnData"]["Equipment"] = TAG_List()
						e["SpawnData"]["Equipment"].append(handitem)
						e["SpawnData"]["Equipment"].append(feetitem)						
						e["SpawnData"]["Equipment"].append(leggingitem)
						e["SpawnData"]["Equipment"].append(chestitem)
						e["SpawnData"]["Equipment"].append(helmetitem)

						if "DropChances" in e["SpawnData"]:
							del e["SpawnData"]["DropChances"]
						e["SpawnData"]["DropChances"] = TAG_List(droplist)

						
						chunk.dirty = True
