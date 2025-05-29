from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String

displayName = "Set Enchant and Color on Mob Equipment"

enchantments = (
	"None",
	"Protection",
	"Fire Protection",
	"Feather Falling",
	"Blast Protection",
	"Projectile Protection",
	"Respiration",
	"Aqua Affinity",
	"Sharpness",
	"Smite",
	"Bane of Arthropods",
	"Knockback",
	"Fire Aspect",
	"Looting",
	"Efficiency",
	"Silk Touch",
	"Unbreaking",
	"Fortune",
	"Power",
	"Punch",
	"Flame",
	"Infinity"
	)
	
enchantment_vals = {
	"None":-1,
	"Protection":0,
	"Fire Protection":1,
	"Feather Falling":2,
	"Blast Protection":3,
	"Projectile Protection":4,
	"Respiration":5,
	"Aqua Affinity":6,
	"Sharpness":16,
	"Smite":17,
	"Bane of Arthropods":18,
	"Knockback":19,
	"Fire Aspect":20,
	"Looting":21,
	"Efficiency":32,
	"Silk Touch":33,
	"Unbreaking":34,
	"Fortune":35,
	"Power":48,
	"Punch":49,
	"Flame":50,
	"Infinity":51
	}

slotvals = {
	"Hand":0,
	"Head":4,
	"Chest":3,
	"Legs":2,
	"Feet":1
	}
	
inputs = (
	("Apply to:", ("Entities","Spawners")),
	("Slot:",("Hand","Head","Chest","Legs","Feet")),
	("Enchantment",enchantments),
	("Enchantment Level",1),
	("Add (Name or Lore):",("None","Overwrite Name","Append Lore","Use Console","Clear Name and Lores")),
	("Name or Lore", "string"),
	("Red color component (0-255)",-1),
	("Green color component (0-255)",-1),
	("Blue color component (0-255)",-1),
	)

def perform(level, box, options):
	applytype = options["Apply to:"]
	
	slot = slotvals[options["Slot:"]]
	enchantment = enchantment_vals[options["Enchantment"]]
	enchantlevel = options["Enchantment Level"]
	red = options["Red color component (0-255)"]
	blue = options["Blue color component (0-255)"]
	green = options["Green color component (0-255)"]
	
	addname = options["Add (Name or Lore):"]
	namelore = options["Name or Lore"]

	if addname != "None":
		lorelist = TAG_List()
		if addname == "Use Console":
			nameval = raw_input("Input Name (hit Enter for none): ")
			while True:
				lorestring = raw_input("Input Lore (hit Enter to stop): ")
				if lorestring == "":
					break
				else:
					lorelist.append(TAG_String(lorestring))
		elif addname == "Append Lore":
			lorelist.append(TAG_String(namelore))
		elif addname == "Overwrite Name":
			nameval = namelore
	
	if red != -1 and blue != -1 and green != -1:
		color = ((red if red != -1 else 0) << 16) | ((green if green != -1 else 0) << 8) | blue if blue != -1 else 0
	else:
		color = -1

	if enchantment >= 0:
		ench = TAG_Compound()
		ench["id"] = TAG_Short(enchantment)
		if enchantlevel > 32767:
			enchantlevel = 32767
		elif enchantlevel < -32768:
			enchantlevel = -32768
		ench["lvl"] = TAG_Short(enchantlevel)
		
	for (chunk, slices, point) in level.getChunkSlices(box):
		if applytype == "Entities":
			for e in chunk.Entities:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
				
				if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
					if "Health" in e:
						if "Equipment" in e:
							if len(e["Equipment"]) == 5:
								if "id" in e["Equipment"][slot]:
									if "tag" not in e["Equipment"][slot]:
										e["Equipment"][slot]["tag"] = TAG_Compound()
									if enchantment >= 0:
										if "ench" not in e["Equipment"][slot]["tag"]:
											e["Equipment"][slot]["tag"]["ench"] = TAG_List()
										e["Equipment"][slot]["tag"]["ench"].append(ench)
										chunk.dirty = True
									if color >= 0 or addname != "None":
										if "display" not in e["Equipment"][slot]["tag"]:
											e["Equipment"][slot]["tag"]["display"] = TAG_Compound()
										if color >= 0:
											e["Equipment"][slot]["tag"]["display"]["color"] = TAG_Int(color)
										if addname != "None":
											if addname == "Overwrite Name":											
												e["Equipment"][slot]["tag"]["display"]["Name"] = TAG_String(nameval)
											elif addname == "Append Lore":
												if "Lore" not in e["Equipment"][slot]["tag"]["display"]:
													e["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
												for L in lorelist:
													e["Equipment"][slot]["tag"]["display"]["Lore"].append(L)
											elif addname == "Use Console":
												if nameval != "":
													e["Equipment"][slot]["tag"]["display"]["Name"] = TAG_String(nameval)
												if "Lore" not in e["Equipment"][slot]["tag"]["display"]:
													e["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
												for L in lorelist:
													e["Equipment"][slot]["tag"]["display"]["Lore"].append(L)
											elif addname == "Clear Name and Lores":
												if "Lore" in e["Equipment"][slot]["tag"]["display"]:
													del e["Equipment"][slot]["tag"]["display"]["Lore"]
												if "Name" in e["Equipment"][slot]["tag"]["display"]:
													del e["Equipment"][slot]["tag"]["display"]["Name"]
										chunk.dirty = True

		else:
			for e in chunk.TileEntities:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
					if e["id"].value == "MobSpawner":
						if "SpawnData" in e:
							if "Equipment" in e["SpawnData"]:
								if len(e["SpawnData"]["Equipment"]) == 5:
									if "id" in e["SpawnData"]["Equipment"][slot]:
										if "tag" not in e["SpawnData"]["Equipment"][slot]:
											e["SpawnData"]["Equipment"][slot]["tag"] = TAG_Compound()
										if enchantment >= 0:
											if "ench" not in e["SpawnData"]["Equipment"][slot]["tag"]:
												e["SpawnData"]["Equipment"][slot]["tag"]["ench"] = TAG_List()
											e["SpawnData"]["Equipment"][slot]["tag"]["ench"].append(ench)
											chunk.dirty = True
										if color >= 0 or addname != "None":
											if "display" not in e["SpawnData"]["Equipment"][slot]["tag"]:
												e["SpawnData"]["Equipment"][slot]["tag"]["display"] = TAG_Compound()
											if color >= 0:
												e["SpawnData"]["Equipment"][slot]["tag"]["display"]["color"] = TAG_Int(color)
											if addname != "None":
												if addname == "Overwrite Name":											
													e["SpawnData"]["Equipment"][slot]["tag"]["display"]["Name"] = TAG_String(nameval)
												elif addname == "Append Lore":
													if "Lore" not in e["SpawnData"]["Equipment"][slot]["tag"]["display"]:
														e["SpawnData"]["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
													for L in lorelist:
														e["SpawnData"]["Equipment"][slot]["tag"]["display"]["Lore"].append(L)
												elif addname == "Use Console":
													if nameval != "":
														e["SpawnData"]["Equipment"][slot]["tag"]["display"]["Name"] = TAG_String(nameval)
													if "Lore" not in e["SpawnData"]["Equipment"][slot]["tag"]["display"]:
														e["SpawnData"]["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
													for L in lorelist:
														e["SpawnData"]["Equipment"][slot]["tag"]["display"]["Lore"].append(L)
												elif addname == "Clear Name and Lores":
													if "Lore" in e["SpawnData"]["Equipment"][slot]["tag"]["display"]:
														del e["SpawnData"]["Equipment"][slot]["tag"]["display"]["Lore"]
													if "Name" in e["SpawnData"]["Equipment"][slot]["tag"]["display"]:
														del e["SpawnData"]["Equipment"][slot]["tag"]["display"]["Name"]
											chunk.dirty = True
