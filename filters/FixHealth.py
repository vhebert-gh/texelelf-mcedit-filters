from pymclevel import TAG_Float, TAG_List, TAG_String, TAG_Double, TAG_Compound

displayName = "Fix Health"

inputs = (("Fix Mob Spawner TileEntities",True),("Fix MinecartSpawner Entities",True),("Fix Mob Entities",True),)

def FixHealth(e):
	if "Health" in e:
		health = float(e["Health"].value)
		e["HealF"] = TAG_Float(health)
		if "Attributes" not in e:
			e["Attributes"] = TAG_List()
		for a in e["Attributes"]:
			if a["Name"].value == "generic.maxHealth":
				a["Base"] = TAG_Double(health)
				break
		else:
			newattrib = TAG_Compound()
			newattrib["Name"] = TAG_String("generic.maxHealth")
			newattrib["Base"] = TAG_Double(health)
			e["Attributes"].append(newattrib)
	if "SpawnData" in e:
		FixHealth(e["SpawnData"])
	if "SpawnPotentials" in e:
		for pot in e["SpawnPotentials"]:
			if "Properties" in pot:
				FixHealth(pot["Properties"])
	if "TileEntityData" in e:
		FixHealth(e["TileEntityData"])
	if "Riding" in e:
		FixHealth(e["Riding"])
 

def perform(level, box, options):
	fixspawners = options["Fix Mob Spawner TileEntities"]
	fixcarts = options["Fix MinecartSpawner Entities"]
	fixmobs = options["Fix Mob Entities"]
	for (chunk, _, _) in level.getChunkSlices(box):
		if fixspawners:
			for e in chunk.TileEntities:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if (x,y,z) in box:
					if e["id"].value == "MobSpawner":
						FixHealth(e)
						chunk.dirty = True
		if fixcarts or fixmobs:
			for e in chunk.Entities:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
				if (x,y,z) in box:
					if e["id"].value == "MinecartSpawner" and fixcarts:
						FixHealth(e)
						chunk.dirty = True
					elif fixmobs:
						FixHealth(e)
						chunk.dirty = True
