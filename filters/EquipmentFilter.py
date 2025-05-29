import uuid
from copy import deepcopy
from pymclevel import TAG_List, TAG_Compound, TAG_String, TAG_Byte, TAG_Short, TAG_Int, TAG_Long, TAG_Float, TAG_Double

displayName = "Complete Mob Equipment Filter"

monsters = ("All","Bat","Blaze","CaveSpider","Chicken","Cow","Creeper","EnderDragon",
			"Enderman","Ghast","Giant","LavaSlime","MushroomCow","Ozelot","Pig","PigZombie",
			"Silverfish","Sheep","Skeleton","Slime","SnowMan","Spider","Squid",
			"Villager","VillagerGolem","Witch","WitherBoss","Wolf","Zombie",)

enchantments = ("None","Protection","Fire Protection","Feather Falling","Blast Protection","Projectile Protection","Respiration","Aqua Affinity","Thorns","Sharpness",
				"Smite","Bane of Arthropods","Knockback","Fire Aspect","Looting","Efficiency","Silk Touch","Unbreaking","Fortune","Power","Punch","Flame","Infinity")
	
enchantment_vals = {"None":-1,"Protection":0,"Fire Protection":1,"Feather Falling":2,"Blast Protection":3,"Projectile Protection":4,"Respiration":5,"Aqua Affinity":6,
					"Thorns":7,"Sharpness":16,"Smite":17,"Bane of Arthropods":18,"Knockback":19,"Fire Aspect":20,"Looting":21,"Efficiency":32,"Silk Touch":33,"Unbreaking":34,
					"Fortune":35,"Power":48,"Punch":49,"Flame":50,"Infinity":51}

potion_effects = (	"None","Speed","Slowness","Haste","Mining Fatigue","Strength","Instant Health",
					"Instant Damage","Jump Boost","Nausea","Regeneration","Resistance","Fire Resistance",
					"Water Breathing","Invisibility","Blindness","Night Vision","Hunger","Weakness",
					"Poison","Wither","Health Boost","Absorption","Saturation")

potion_effects_vals = {	"None": -1,"Speed": 1,"Slowness": 2,"Haste": 3,"Mining Fatigue": 4,"Strength": 5,"Instant Health": 6,"Instant Damage": 7,
						"Jump Boost": 8,"Nausea": 9,"Regeneration": 10,"Resistance": 11,"Fire Resistance": 12,"Water Breathing": 13,"Invisibility": 14,
						"Blindness": 15,"Night Vision": 16,"Hunger": 17,"Weakness": 18,"Poison": 19,"Wither": 20,"Health Boost":21,"Absorption":22,"Saturation":23}
	
slotvals = {"Hand":0,"Head":4,"Chest":3,"Legs":2,"Feet":1}
slotkeys = ["Hand","Feet","Legs","Chest","Head"]

sectional = "\xA7"

def checkid(entity, slot, id):
	if "Equipment" in entity:
		if len(entity["Equipment"]) >= slot:
			if "id" in entity["Equipment"][slot]:
				if entity["Equipment"][slot]["id"].value == id:
					return True
	return False

def checkname(entity, slot, name):
	if "Equipment" in entity:
		if len(entity["Equipment"]) >= slot:
			if "tag" in entity["Equipment"][slot]:
				if "display" in entity["Equipment"][slot]["tag"]:
					if "Name" in entity["Equipment"][slot]["tag"]["display"]:
						if entity["Equipment"][slot]["tag"]["display"]["Name"].value == name:
							return True
	return False
	
inputs = [
	(("Apply to:", ("Entities","Spawners","Spawner Minecarts")),
	("Spawner Slot (0 for all slots):",0),
	("Slot:",("Hand","Head","Chest","Legs","Feet")),
	("Operation:",(	"Set All",
					"Set ID, Damage, and Count Only",
					"Set Repair Cost Only",
					"Add Enchantment Only",
					"Add Potion Effect Only",
					"Set Name Only",
					"Prefix Lore Only",
					"Add Lore Only",
					"Set Drop Rate Only",
					"Set Dye Color Only",
					"Use Name to Set Player's Skull",
					"Add or Edit Attribute Modifier",
					"List Attributes in Console",
					"Set Unbreakability",
					"Remove Item from Slot",
					"Remove Repair Cost",
					"Remove Enchants",
					"Remove Potion Effects",
					"Remove Name",
					"Remove Lores",
					"Remove Attribute Modifiers",
					"List Spawn Slots in Console",)),
	("Only apply to Mob:",monsters),
	("Apply only if Item ID matches",False),
	("Apply only if Name matches",False),
	("Item ID:",(0,-32768,32767)),
	("Item Damage:",(0,-32768,32767)),
	("Item Count:",(1,-128,127)),
	("Item Drop Rate (Percentage; 200 to drop undamaged):",(5,0,1000)),
	("Item is Unbreakable:",False),
	("Item Repair Cost (-1 to ignore)",(-1,-2147483648,2147483647)),
	("Enchantment",enchantments),
	("Enchantment Level",(1,-32768,32767)),
	("Potion Effect (ID MUST be 373!)",potion_effects),
	("Potion Level", (1,-128, 127)),
	("Potion Duration (Seconds)", (0, 0, 107374181)),
	("Use \"None\" for Name and\\or Lore below to ignore","label"),
	("Name",("string","value=None")),
	("Lore",("string","value=None")),
	("Use Leather Dye Color",False),
	("Dye Color (hex: #RRGGBB or dec: RRR,GGG,BBB)",("string","value=#5C4033")),
	("General Settings","title"),),
	
	(("Attribute to Add or Modify:",(	"Custom",
										"generic.maxHealth",
										"generic.followRange",
										"generic.knockbackResistance",
										"generic.movementSpeed",
										"generic.attackDamage",
										"horse.jumpStrength",
										"zombie.spawnReinforcements"
									)),
	("Custom Attribute's Name:",("string","value=None")),
	("Modifier Name:",("string","value=None")),
	("Modifier Amount:",0.0),
	("X = Attribute's Base value\nY = X, usually the Result of the previous Operation if there was one (0's result for 1, 1's result for 2, etc.)\n0: X + Amount\n1: Y + (X * Amount)\n2: Y * (1 + Amount","label"),
	("Modifier Operation:",(0,-2147483648,2147483647)),
	("\n\n\n","label"),
	("The UUID fields below are valid only for Item Attributes or for Attribute Modifiers.","label"), 
	("UUID:",("Generate Random UUID","Use UUID Least and Most","Use UUID String")),
	("UUID Least:",(0,-9223372036854775808,9223372036854775807)),
	("UUID Most:",(0,-9223372036854775808,9223372036854775807)),
	("UUID String:",("string","value=None")),
	("Attributes","title"),),
	]

def perform(level, box, options):
	applytype = options["Apply to:"]
	spawnslot = options["Spawner Slot (0 for all slots):"]-1
	slot = slotvals[options["Slot:"]]
	op = options["Operation:"]
	mob = options["Only apply to Mob:"]
	enchantment = enchantment_vals[options["Enchantment"]]
	enchantlevel = options["Enchantment Level"]
	usedye = options["Use Leather Dye Color"]
	dyestring = options["Dye Color (hex: #RRGGBB or dec: RRR,GGG,BBB)"]
	
	idmatch = options["Apply only if Item ID matches"]
	namematch = options["Apply only if Name matches"]
	
	id = options["Item ID:"]
	damage = options["Item Damage:"]
	count = options["Item Count:"]
	rate = options["Item Drop Rate (Percentage; 200 to drop undamaged):"]
	unbreakable = options["Item is Unbreakable:"]
	repair = options["Item Repair Cost (-1 to ignore)"]
	
	potioneffect = potion_effects_vals[options["Potion Effect (ID MUST be 373!)"]]
	potionlevel = options["Potion Level"]
	potionduration = options["Potion Duration (Seconds)"]

	defattrib = options["Attribute to Add or Modify:"]
	custattrib = options["Custom Attribute's Name:"]
	if defattrib == "Custom":
		attribname = custattrib
	else:
		attribname = defattrib
	modname = options["Modifier Name:"]
	modamount = options["Modifier Amount:"]
	modop = options["Modifier Operation:"]
	uuidgen = options["UUID:"]
	uuidleast = options["UUID Least:"]
	uuidmost = options["UUID Most:"]
	uuidstr = options["UUID String:"]
	if uuidgen == "Use UUID String" and uuidstr == "None":
		uuidgen = "Generate Random UUID"
	
	name = options["Name"]
	lore = options["Lore"]
	if name == "None":
		name = ""
	if lore == "None":
		lore = ""
	if name != "":
		name = name.encode("unicode-escape")
		name = name.replace("|",sectional)
		name = name.decode("unicode-escape")
	if lore != "":
		lore = lore.encode("unicode-escape")
		lore = lore.replace("|",sectional)
		lore = lore.decode("unicode-escape")
		
	if potioneffect != -1:
		potion = TAG_Compound()
		potion["Amplifier"] = TAG_Byte(potionlevel-1)
		potion["Id"] = TAG_Byte(potioneffect)
		potion["Duration"] = TAG_Int(potionduration * 20)

	if rate == 5:
		rate = 0.05000000074505806
	else:
		rate *= 0.01	
	
	if op == "Set Dye Color Only":
		usedye = True
	if usedye:
		if dyestring[0] == "#":
			color = int(dyestring[1:],16)
		elif len(dyestring.split(",")) == 3:
			(red,green,blue) = dyestring.split(",")
			red = int(red)
			green = int(green)
			blue = int(blue)
			color = (red << 16) | (green << 8) | blue
		else:
			usedye = False

	if enchantment >= 0:
		ench = TAG_Compound()
		ench["id"] = TAG_Short(enchantment)
		ench["lvl"] = TAG_Short(enchantlevel)

	for (chunk, slices, point) in level.getChunkSlices(box):
		if applytype == "Entities":
			for e in chunk.Entities:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
				
				if (x,y,z) in box:
					if "Health" in e:

						if mob != "All" and e["EntityId"].value != mob:
							continue
					
						if namematch:
							if not checkname(e,slot,name):
								continue
						if idmatch:
							if not checkid(e,slot,id):
								continue

						if "Equipment" not in e:
							e["Equipment"] = TAG_List()
						if len(e["Equipment"]) < 5:
							for a in xrange(len(e["Equipment"]),5):
								e["Equipment"].append(TAG_Compound())

						if "DropChances" not in e:
							e["DropChances"] = TAG_List()
						if len(e["DropChances"]) < 5:
							for a in xrange(len(e["DropChances"]),5):
								e["DropChances"].append(TAG_Float(0.05000000074505806))
						if "Remove" in op:
							if op == "Remove Item from Slot":
								e["Equipment"][slot] = TAG_Compound()
								e["DropChances"][slot] = TAG_Float(0.05000000074505806)
								chunk.dirty = True

							elif op == "Remove Repair Cost":
								if "tag" in e["Equipment"][slot]:
									if "RepairCost" in e["Equipment"][slot]["tag"]:
										del e["Equipment"][slot]["tag"]["RepairCost"]

							elif op == "Remove Name":
								if "tag" in e["Equipment"][slot]:
									if "display" in e["Equipment"][slot]["tag"]:
										if "Name" in e["Equipment"][slot]["tag"]["display"]:
											del e["Equipment"][slot]["tag"]["display"]["Name"]
											chunk.dirty = True
							elif op == "Remove Lores":
								if "tag" in e["Equipment"][slot]:
									if "display" in e["Equipment"][slot]["tag"]:
										if "Lore" in e["Equipment"][slot]["tag"]["display"]:
											del e["Equipment"][slot]["tag"]["display"]["Lore"]
											chunk.dirty = True
							elif op == "Remove Enchants":
								if "tag" in e["Equipment"][slot]:
									if "ench" in e["Equipment"][slot]["tag"]:
										del e["Equipment"][slot]["tag"]["ench"]
										chunk.dirty = True
							elif op == "Remove Potion Effects":
								if "tag" in e["Equipment"][slot]:
									if "CustomPotionEffects" in e["Equipment"][slot]["tag"]:
										del e["Equipment"][slot]["tag"]["CustomPotionEffects"]
										chunk.dirty = True
							elif op == "Remove Attribute Modifiers":
								if "tag" in e["Equipment"][slot]:
									if "AttributeModifiers" in e["Equipment"][slot]["tag"]:
										del e["Equipment"][slot]["tag"]["AttributeModifiers"]
										chunk.dirty = True

						elif op == "Set All":
							e["DropChances"][slot] = TAG_Float(rate)
							e["Equipment"][slot]["id"] = TAG_Short(id)
							e["Equipment"][slot]["Damage"] = TAG_Short(damage)
							e["Equipment"][slot]["Count"] = TAG_Byte(count)
							if "tag" in e["Equipment"][slot]:
								del e["Equipment"][slot]["tag"]
							if enchantment >= 0 or (potioneffect != -1 and id == 373) or repair != -1 or usedye or name != "" or lore != "" or unbreakable:
								e["Equipment"][slot]["tag"] = TAG_Compound()
							if unbreakable:
								e["Equipment"][slot]["tag"]["Unbreakable"] = TAG_Byte(unbreakable)
							if enchantment >= 0:
								e["Equipment"][slot]["tag"]["ench"] = TAG_List()
								e["Equipment"][slot]["tag"]["ench"].append(ench)
							if potioneffect != -1 and id == 373:
								e["Equipment"][slot]["tag"]["CustomPotionEffects"] = TAG_List()
								e["Equipment"][slot]["tag"]["CustomPotionEffects"].append(potion)
							if repair != -1:
								e["Equipment"][slot]["tag"]["RepairCost"] = TAG_Int(repair)

							if usedye or name != "" or lore != "":
								e["Equipment"][slot]["tag"]["display"] = TAG_Compound()
								if usedye:
									e["Equipment"][slot]["tag"]["display"]["color"] = TAG_Int(color)
								if name != "":
									e["Equipment"][slot]["tag"]["display"]["Name"] = TAG_String(name)
								if lore != "":
									e["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
									e["Equipment"][slot]["tag"]["display"]["Lore"].append(TAG_String(lore))
							chunk.dirty = True

						else:
							if op == "Set ID, Damage, and Count Only":
								e["Equipment"][slot]["id"] = TAG_Short(id)
								e["Equipment"][slot]["Damage"] = TAG_Short(damage)
								e["Equipment"][slot]["Count"] = TAG_Byte(count)
								chunk.dirty = True
							else:
								if "id" in e["Equipment"][slot] or op == "Use Name to Set Player's Skull":
									if op == "Add Enchantment Only" and enchantment >= 0:
										if "tag" not in e["Equipment"][slot]:
											e["Equipment"][slot]["tag"] = TAG_Compound()
										if "ench" not in e["Equipment"][slot]["tag"]:
											e["Equipment"][slot]["tag"]["ench"] = TAG_List()
										e["Equipment"][slot]["tag"]["ench"].append(ench)
										chunk.dirty = True
									elif op == "Set Repair Cost Only" and repair != -1:
										if "tag" not in e["Equipment"][slot]:
											e["Equipment"][slot]["tag"] = TAG_Compound()
										e["Equipment"][slot]["tag"]["RepairCost"] = TAG_Int(repair)
										chunk.dirty = True
									elif op == "Add Potion Effect Only":
										if potioneffect != -1 and e["Equipment"][slot]["id"].value == 373:
											if "tag" not in e["Equipment"][slot]:
												e["Equipment"][slot]["tag"] = TAG_Compound()
											if "CustomPotionEffects" not in e["Equipment"][slot]["tag"]:
												e["Equipment"][slot]["tag"]["CustomPotionEffects"] = TAG_List()
											e["Equipment"][slot]["tag"]["CustomPotionEffects"].append(potion)
											chunk.dirty = True
									elif op == "Set Name Only" and name != "":
										if "tag" not in e["Equipment"][slot]:
											e["Equipment"][slot]["tag"] = TAG_Compound()
										if "display" not in e["Equipment"][slot]["tag"]:
											e["Equipment"][slot]["tag"]["display"] = TAG_Compound()
										if "Lore" not in e["Equipment"][slot]["tag"]["display"]:
											e["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
										e["Equipment"][slot]["tag"]["display"]["Name"] = TAG_String(name)
										chunk.dirty = True
									elif op == "Add Lore Only" and lore != "":
										if "tag" not in e["Equipment"][slot]:
											e["Equipment"][slot]["tag"] = TAG_Compound()
										if "display" not in e["Equipment"][slot]["tag"]:
											e["Equipment"][slot]["tag"]["display"] = TAG_Compound()
										if "Lore" not in e["Equipment"][slot]["tag"]["display"]:
											e["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
										e["Equipment"][slot]["tag"]["display"]["Lore"].append(TAG_String(lore))
										chunk.dirty = True
									elif op == "Set Unbreakability":
										if "tag" not in e["Equipment"][slot]:
											e["Equipment"][slot]["tag"] = TAG_Compound()
										e["Equipment"][slot]["tag"]["Unbreakable"] = TAG_Byte(unbreakable)
										chunk.dirty = True
									elif op == "Set Drop Rate Only":
										e["DropChances"][slot] = TAG_Float(rate)
										chunk.dirty = True
									elif op == "Set Dye Color Only" and usedye:
										if "tag" not in e["Equipment"][slot]:
											e["Equipment"][slot]["tag"] = TAG_Compound()
										if "display" not in e["Equipment"][slot]["tag"]:
											e["Equipment"][slot]["tag"]["display"] = TAG_Compound()
										e["Equipment"][slot]["tag"]["display"]["color"] = TAG_Int(color)
										chunk.dirty = True
									elif op == "Use Name to Set Player's Skull" and name != "":
										e["Equipment"][slot]["id"] = TAG_Short(397)
										e["Equipment"][slot]["Damage"] = TAG_Short(3)
										e["Equipment"][slot]["Count"] = TAG_Byte(count)
										e["DropChances"][slot] = TAG_Float(rate)
										if "tag" not in e["Equipment"][slot]:
											e["Equipment"][slot]["tag"] = TAG_Compound()
										e["Equipment"][slot]["tag"]["SkullOwner"] = TAG_String(name)
										chunk.dirty = True

									elif op == "Add or Edit Attribute Modifier":
											if "tag" not in e["Equipment"][slot]:
												e["Equipment"][slot]["tag"] = TAG_Compound()
											if "AttributeModifiers" not in e["Equipment"][slot]["tag"]:
												e["Equipment"][slot]["tag"]["AttributeModifiers"] = TAG_List()
											for a in e["Equipment"][slot]["tag"]["AttributeModifiers"]:
												if a["AttributeName"].value == attribname:
													a["Amount"] = TAG_Double(modamount)
													a["Operation"] = TAG_Int(modop)
													break
											else:
												attrib = TAG_Compound()
												attrib["Name"] = TAG_String(modname)
												attrib["AttributeName"] = TAG_String(attribname)
												attrib["Amount"] = TAG_Double(modamount)
												attrib["Operation"] = TAG_Int(modop)
												if uuidgen == "Generate Random UUID":
													uuidval = uuid.uuid4()
													least = uuidval.int & 0xFFFFFFFFFFFFFFFF
													most = uuidval.int >> 64
													if least > 9223372036854775807:
														least = least - 18446744073709551616
													if most > 9223372036854775807:
														most = most - 18446744073709551616
												elif uuidgen == "Use UUID Least and Most":
													least = uuidleast
													most = uuidmost
												elif uuidgen == "Use UUID String":
													uuidval = uuid.UUID(uuidstr)
													least = uuidval.int & 0xFFFFFFFFFFFFFFFF
													most = uuidval.int >> 64
													if least > 9223372036854775807:
														least = least - 18446744073709551616
													if most > 9223372036854775807:
														most = most - 18446744073709551616
												attrib["UUIDLeast"] = TAG_Long(least)
												attrib["UUIDMost"] = TAG_Long(most)
												e["Equipment"][slot]["tag"]["AttributeModifiers"].append(attrib)
											chunk.dirty = True
									elif op == "List Attributes in Console":
										if "tag" in e["Equipment"][slot]:
											if "AttributeModifiers" in e["Equipment"][slot]["tag"]:
												print "Attribute Modifiers for",e["id"].value,"in Equipment Slot",slotkeys[slot],"of mob at",x,y,z,":"
												for m in e["Equipment"][slot]["tag"]["AttributeModifiers"]:
													print "Modifier:",m["Name"].value,", amount:",str(m["Amount"].value),", operation:",str(m["Operation"].value),","
													print "uuid:",uuid.UUID(int=(((m["UUIDMost"].value & 0xFFFFFFFFFFFFFFFF) << 64) | (m["UUIDLeast"].value& 0xFFFFFFFFFFFFFFFF))).hex

		else:
			for e in chunk.TileEntities if applytype == "Spawners" else chunk.Entities:
				if applytype == "Spawners":
					x = e["x"].value
					y = e["y"].value
					z = e["z"].value
				else:
					x = e["Pos"][0].value
					y = e["Pos"][1].value
					z = e["Pos"][2].value
				if (x,y,z) in box:
					if e["id"].value == "MobSpawner" or e["id"].value == "MinecartSpawner":

						if "SpawnPotentials" not in e:
							if "EntityId" not in e: #ignore undefined spawners
								continue
							if "SpawnData" in e:
								e["SpawnPotentials"] = TAG_List()
								potent = TAG_Compound()
								potent["Weight"] = TAG_Byte(1)
								potent["Type"] = TAG_String(e["EntityId"].value)
								potent["Properties"] = deepcopy(e["SpawnData"])
								print potent
								e["SpawnPotentials"].append(potent)
							else:
								e["SpawnPotentials"] = TAG_List()
								potent = TAG_Compound()
								potent["Weight"] = TAG_Byte(1)
								potent["Type"] = TAG_String(e["EntityId"].value)
								potent["Properties"] = TAG_Compound()
								e["SpawnPotentials"].append(potent)
						if op == "List Spawn Slots in Console":
							slotcounter = 0
							print "Spawner at: X "+str(x)+", Y "+str(y)+", Z "+str(z)
							for ent in e["SpawnPotentials"]:
								slotcounter += 1
								print str(slotcounter)+": "+ str(ent["Type"].value) +", weight: "+str(ent["Weight"].value)
						if len(e["SpawnPotentials"])-1 < spawnslot:
							continue
						for i in xrange(0 if spawnslot == -1 else spawnslot, len(e["SpawnPotentials"]) if spawnslot == -1 else spawnslot+1):

							if e["SpawnPotentials"][i]["Type"].value not in monsters: #ignore entity spawners
								continue

							if mob != "All" and e["SpawnPotentials"][i]["Type"].value != mob:
								continue
								
							if namematch:
								if not checkname(e["SpawnPotentials"][i]["Properties"],slot,name):
									continue
							if idmatch:
								if not checkid(e["SpawnPotentials"][i]["Properties"],slot,id):
									continue

							if "Equipment" not in e["SpawnPotentials"][i]["Properties"]:
								e["SpawnPotentials"][i]["Properties"]["Equipment"] = TAG_List()
							if len(e["SpawnPotentials"][i]["Properties"]["Equipment"]) < 5:
								for a in xrange(len(e["SpawnPotentials"][i]["Properties"]["Equipment"]),5):
									e["SpawnPotentials"][i]["Properties"]["Equipment"].append(TAG_Compound())

							if "DropChances" not in e["SpawnPotentials"][i]["Properties"]:
								e["SpawnPotentials"][i]["Properties"]["DropChances"] = TAG_List()
							if len(e["SpawnPotentials"][i]["Properties"]["DropChances"]) < 5:
								for a in xrange(len(e["SpawnPotentials"][i]["Properties"]["DropChances"]),5):
									e["SpawnPotentials"][i]["Properties"]["DropChances"].append(TAG_Float(0.05000000074505806))
									
							if "Remove" in op:
								if op == "Remove Item from Slot":
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot] = TAG_Compound()
									e["SpawnPotentials"][i]["Properties"]["DropChances"][slot] = TAG_Float(0.05000000074505806)
									chunk.dirty = True
								elif op == "Remove Repair Cost":
									if "tag" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
										if "RepairCost" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
											del e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["RepairCost"]
								elif op == "Remove Name":
									if "tag" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
										if "display" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
											if "Name" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]:
												del e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Name"]
												chunk.dirty = True
								elif op == "Remove Lores":
									if "tag" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
										if "display" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
											if "Lore" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]:
												del e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Lore"]
												chunk.dirty = True
								elif op == "Remove Enchants":
									if "tag" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
										if "ench" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
											del e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["ench"]
											chunk.dirty = True
								elif op == "Remove Potion Effects":
									if "tag" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
										if "CustomPotionEffects" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
											del e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["CustomPotionEffects"]
											chunk.dirty = True
								elif op == "Remove Attribute Modifiers":
									if "tag" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
										if "AttributeModifiers" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
											del e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["AttributeModifiers"]
											chunk.dirty = True
							elif op == "Set All":
								e["SpawnPotentials"][i]["Properties"]["DropChances"][slot] = TAG_Float(rate)
								e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["id"] = TAG_Short(id)
								e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["Damage"] = TAG_Short(damage)
								e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["Count"] = TAG_Byte(count)
								if "tag" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
									del e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]
								if enchantment >= 0 or (potioneffect != -1 and id == 373) or repair != -1 or usedye or name != "" or lore != "" or unbreakable:
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
								if unbreakable:
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["Unbreakable"] = TAG_Byte(unbreakable)
								if enchantment >= 0:
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["ench"] = TAG_List()
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["ench"].append(ench)
								if potioneffect != -1 and id == 373:
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["CustomPotionEffects"] = TAG_List()
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["CustomPotionEffects"].append(potion)
								if repair != -1:
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["RepairCost"] = TAG_Int(repair)

								if usedye or name != "" or lore != "":
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"] = TAG_Compound()
									if usedye:
										e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["color"] = TAG_Int(color)
									if name != "":
										e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Name"] = TAG_String(name)
									if lore != "":
										e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
										e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Lore"].append(TAG_String(lore))
								chunk.dirty = True

							else:
								if op == "Set ID, Damage, and Count Only":
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["id"] = TAG_Short(id)
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["Damage"] = TAG_Short(damage)
									e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["Count"] = TAG_Byte(count)
									chunk.dirty = True
								else:
									if "id" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot] or op == "Use Name to Set Player's Skull":
										if op == "Add Enchantment Only" and enchantment >= 0:
											if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
											if "ench" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["ench"] = TAG_List()
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["ench"].append(ench)
											chunk.dirty = True
										elif op == "Set Repair Cost Only" and repair != -1:
											if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["RepairCost"] = TAG_Int(repair)
											chunk.dirty = True
										elif op == "Add Potion Effect Only":
											if potioneffect != -1 and e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["id"].value == 373:
												if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
													e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
												if "CustomPotionEffects" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
													e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["CustomPotionEffects"] = TAG_List()
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["CustomPotionEffects"].append(potion)
												chunk.dirty = True
										elif op == "Set Name Only" and name != "":
											if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
											if "display" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"] = TAG_Compound()
											if "Lore" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Name"] = TAG_String(name)
											chunk.dirty = True
										elif op == "Add Lore Only" and lore != "":
											if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
											if "display" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"] = TAG_Compound()
											if "Lore" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Lore"].append(TAG_String(lore))
											chunk.dirty = True
										elif op == "Prefix Lore Only" and lore != "":
											if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
											if "display" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"] = TAG_Compound()
											if "Lore" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Lore"] = TAG_List()
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["Lore"].insert(0,TAG_String(lore))
											chunk.dirty = True
										elif op == "Set Unbreakability":
											if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["Unbreakable"] = TAG_Byte(unbreakable)
											chunk.dirty = True
										elif op == "Set Drop Rate Only":
											e["SpawnPotentials"][i]["Properties"]["DropChances"][slot] = TAG_Float(rate)
											chunk.dirty = True
										elif op == "Set Dye Color Only" and usedye:
											if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
											if "display" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"] = TAG_Compound()
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["display"]["color"] = TAG_Int(color)
											chunk.dirty = True
										elif op == "Use Name to Set Player's Skull":
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["id"] = TAG_Short(397)
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["Damage"] = TAG_Short(3)
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["Count"] = TAG_Byte(count)
											e["SpawnPotentials"][i]["Properties"]["DropChances"][slot] = TAG_Float(rate)
											if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
											e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["SkullOwner"] = TAG_String(name)
											chunk.dirty = True
											
										elif op == "Add or Edit Attribute Modifier":
											if "tag" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"] = TAG_Compound()
											if "AttributeModifiers" not in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["AttributeModifiers"] = TAG_List()
											for a in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["AttributeModifiers"]:
												if a["AttributeName"].value == attribname:
													a["Amount"] = TAG_Double(modamount)
													a["Operation"] = TAG_Int(modop)
													break
											else:
												attrib = TAG_Compound()
												attrib["Name"] = TAG_String(modname)
												attrib["AttributeName"] = TAG_String(attribname)
												attrib["Amount"] = TAG_Double(modamount)
												attrib["Operation"] = TAG_Int(modop)
												if uuidgen == "Generate Random UUID":
													uuidval = uuid.uuid4()
													least = uuidval.int & 0xFFFFFFFFFFFFFFFF
													most = uuidval.int >> 64
													if least > 9223372036854775807:
														least = least - 18446744073709551616
													if most > 9223372036854775807:
														most = most - 18446744073709551616
												elif uuidgen == "Use UUID Least and Most":
													least = uuidleast
													most = uuidmost
												elif uuidgen == "Use UUID String":
													uuidval = uuid.UUID(uuidstr)
													least = uuidval.int & 0xFFFFFFFFFFFFFFFF
													most = uuidval.int >> 64
													if least > 9223372036854775807:
														least = least - 18446744073709551616
													if most > 9223372036854775807:
														most = most - 18446744073709551616
												attrib["UUIDLeast"] = TAG_Long(least)
												attrib["UUIDMost"] = TAG_Long(most)
												e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["AttributeModifiers"].append(attrib)
											chunk.dirty = True
										elif op == "List Attributes in Console":
											if "tag" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]:
												if "AttributeModifiers" in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]:
													print "Attribute Modifiers for",e["SpawnPotentials"][i]["Type"].value,"in Equipment Slot",slotkeys[slot],"of spawner at",x,y,z,":"
													for m in e["SpawnPotentials"][i]["Properties"]["Equipment"][slot]["tag"]["AttributeModifiers"]:
														print "Modifier:",m["Name"].value,", amount:",str(m["Amount"].value),", operation:",str(m["Operation"].value),","
														print "uuid:",uuid.UUID(int=(((m["UUIDMost"].value & 0xFFFFFFFFFFFFFFFF) << 64) | (m["UUIDLeast"].value& 0xFFFFFFFFFFFFFFFF))).hex
											
						e["SpawnData"] = deepcopy(e["SpawnPotentials"][spawnslot if spawnslot > -1 else 0]["Properties"])
						e["EntityId"] = TAG_String(e["SpawnPotentials"][spawnslot if spawnslot > -1 else 0]["Type"].value)