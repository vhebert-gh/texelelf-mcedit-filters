from pymclevel import TAG_Short, TAG_Byte, TAG_String, TAG_Compound
from copy import deepcopy

displayName = "Fix Shops"

inputs = (
	("Old Trade Disablement ID",(36,0,32767)),
	("New Trade Disablement ID",(90,0,32767)),
	("New Trade Disablement Count",(99,0,127)),
	("New Trade Disablement Label",("string","value=No More Trades Available")),
	)

def DeleteTrade(e,old,new,count,label):
	if "Offers" not in e:
		return False
	if "Recipes" not in e["Offers"]:
		return False
	if len(e["Offers"]["Recipes"]) <= 0:
		return False
	if e["Offers"]["Recipes"][-1]["buy"]["id"].value == old:
		e["Offers"]["Recipes"][-1]["buy"]["id"] = TAG_Short(new)
		e["Offers"]["Recipes"][-1]["buy"]["Damage"] = TAG_Short(0)
		e["Offers"]["Recipes"][-1]["buy"]["Count"] = TAG_Byte(count)
		if "tag" in e["Offers"]["Recipes"][-1]["buy"]:
			del e["Offers"]["Recipes"][-1]["buy"]["tag"]
		e["Offers"]["Recipes"][-1]["buy"]["tag"] = TAG_Compound()
		e["Offers"]["Recipes"][-1]["buy"]["tag"]["display"] = TAG_Compound()
		e["Offers"]["Recipes"][-1]["buy"]["tag"]["display"]["Name"] = TAG_String(label)
		if "buyB" in e["Offers"]["Recipes"][-1]:
			del e["Offers"]["Recipes"][-1]["buyB"]
		e["Offers"]["Recipes"][-1]["sell"] = deepcopy(e["Offers"]["Recipes"][-1]["buy"])
		return True
	else:
		return False


def perform(level, box, options):
	old = options["Old Trade Disablement ID"]
	new = options["New Trade Disablement ID"]
	count = options["New Trade Disablement Count"]
	label = options["New Trade Disablement Label"]
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.Entities:
			x = e["Pos"][0].value
			y = e["Pos"][1].value
			z = e["Pos"][2].value
			if (x,y,z) in box:
				if "id" not in e:
					continue
				if e["id"].value == "Villager":
					if DeleteTrade(e,old,new,count,label):
						chunk.dirty = True
				elif e["id"].value == "MinecartSpawner":
					if e["EntityId"].value == "Villager":
						if "SpawnData" in e:
							if DeleteTrade(e["SpawnData"],old,new,count,label):
								chunk.dirty = True
						elif "Properties" in e:
							if DeleteTrade(e["Properties"],old,new,count,label):
								chunk.dirty = True
					if "SpawnPotentials" in e:
						for pot in e["SpawnPotentials"]:
							if pot["Type"].value == "Villager":
								if DeleteTrade(pot["Properties"],old,new,count,label):
									chunk.dirty = True				
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:
				if "id" not in e:
					continue
				if e["id"].value != "MobSpawner":
					continue
				if e["EntityId"].value == "Villager":
					if "SpawnData" in e:
						if DeleteTrade(e["SpawnData"],old,new,count,label):
							chunk.dirty = True
					elif "Properties" in e:
						if DeleteTrade(e["Properties"],old,new,count,label):
							chunk.dirty = True
				if "SpawnPotentials" in e:
					for pot in e["SpawnPotentials"]:
						if pot["Type"].value == "Villager":
							if DeleteTrade(pot["Properties"],old,new,count,label):
								chunk.dirty = True
