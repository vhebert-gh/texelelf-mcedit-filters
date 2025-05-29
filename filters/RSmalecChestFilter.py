import uuid
from copy import deepcopy
from pymclevel import TAG_List, TAG_Compound, TAG_String, TAG_Byte, TAG_Short, TAG_Int, TAG_Long, TAG_Float, TAG_Double

displayName = "RSmalec's Chest Filter"

types = {	"All Block Containers":"All Block Containers","All Minecart Containers":"All Minecart Containers","Chest":"Chest","Dispenser":"Trap","Dropper":"Dropper","Hopper":"Hopper","Furnace":"Furnace","Brewing Stand":"Cauldron",
			"Storage Minecart":"MinecartChest","Furnace Minecart":"MinecartFurnace","Hopper Minecart":"MinecartHopper","Horses, Mules, and Donkeys":"EntityHorse"}

capacities = {	"Chest":27,"Trap":9,"Dropper":9,"Hopper":5,"Furnace":3,"Cauldron":4,
				"MinecartChest":27,"MinecartFurnace":3,"MinecartHopper":5,"EntityHorse":15}

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

sectional = "\xA7"

def checkname(item, name):
	if "tag" in item:
		if "display" in item["tag"]:
			if "Name" in item["tag"]["display"]:
				if item["tag"]["display"]["Name"].value == name:
					return True
	return False
	
inputs = [
	(("Apply to:", tuple(sorted(types.keys()))),
	("Operation:",(	"Fill Container",
					"Add Item to Slot",
					"Set All",
					"Set ID, Damage, and Count Only",
					"Set Repair Cost Only",
					"Add Enchantment Only",
					"Add Potion Effect Only",
					"Set Item Name Only",
					"Prefix Lore Only",
					"Add Item Lore Only",
					"Set Container Name Only",
					"Set Dye Color Only",
					"Add or Edit Attribute Modifier",
					"List Attributes in Console",
					"Set Unbreakability",
					"Set Breakable Block List",
					"Append to Breakable Block List",
					"Set Placeable Block List",
					"Append to Placeable Block List",
					"Empty Container",
					"Remove Item",
					"Remove Repair Cost",
					"Remove Enchants",
					"Remove Potion Effects",
					"Remove Item Name",
					"Remove Item Lores",
					"Remove Container Name",
					"Remove Attribute Modifier",
					"Find Items Matching Below")),
	("Only if Item Slot matches",False),
	("Only if Item ID matches",False),
	("Only if Item Damage matches",False),
	("Only if Item Count matches",False),
	("Only if Item Name matches",False),
	("Item ID:",("string","value=minecraft:")),
	("Item Damage:",(0,-32768,32767)),
	("Item Count:",(1,-128,127)),
	("Item Slot:",(0,-128,127)),
	("Item is Unbreakable:",False),
	("Item Repair Cost (-1 to ignore)",(-1,-2147483648,2147483647)),
	("Enchantment:",enchantments),
	("Enchantment Level:",(1,-32768,32767)),
	("Potion Effect:",potion_effects),
	("Potion Level:", (1,-128, 127)),
	("Potion Duration (Seconds):", (0, 0, 107374181)),
	("Use \"None\" for Name and\\or Lore below to ignore","label"),
	("Item Name",("string","value=None")),
	("Item Lore",("string","value=None")),
	("Container Name",("string","value=None")),
	("Use Leather Dye Color",False),
	("Dye Color (hex: #RRGGBB or dec: RRR,GGG,BBB)",("string","value=#5C4033")),
	("Container Settings","title"),),
	
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
	("Modifier Operation:",(0,0,2147483647)),
	("\n\n\n","label"),
	("The UUID fields below are valid only for Item Attributes or for Attribute Modifiers.","label"), 
	("UUID:",("Generate Random UUID","Use UUID Least and Most","Use UUID String")),
	("UUID Least:",(0,-9223372036854775808,9223372036854775807)),
	("UUID Most:",(0,-9223372036854775808,9223372036854775807)),
	("UUID String:",("string","value=None")),
	("Attributes","title"),),
	
	(("The following two options are comma-separated lists of block IDs.\nE.g.:\nminecraft:grass,minecraft:stone,minecraft:dirt","label"),
	("Can Break:",("string","value=None","width=700")),
	("Can Place On:",("string","value=None","width=700")),
	("Adventure","title"),),
	]

def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def perform(level, box, options):
	applytype = types[options["Apply to:"]]
	slt = options["Item Slot:"]
	op = options["Operation:"]
	enchantment = enchantment_vals[options["Enchantment:"]]
	enchantlevel = options["Enchantment Level:"]
	usedye = options["Use Leather Dye Color"]
	dyestring = options["Dye Color (hex: #RRGGBB or dec: RRR,GGG,BBB)"]
	
	slotmatch = options["Only if Item Slot matches"]
	idmatch = options["Only if Item ID matches"]
	damagematch = options["Only if Item Damage matches"]
	countmatch = options["Only if Item Count matches"]
	namematch = options["Only if Item Name matches"]
	
	id = options["Item ID:"]
	if isNumber(id):
		shortVal = True
		id = int(id)
	else:
		shortVal = False

	damage = options["Item Damage:"]
	count = options["Item Count:"]
	unbreakable = options["Item is Unbreakable:"]
	repair = options["Item Repair Cost (-1 to ignore)"]
	
	potioneffect = potion_effects_vals[options["Potion Effect:"]]
	potionlevel = options["Potion Level:"]
	potionduration = options["Potion Duration (Seconds):"]

	if applytype == "EntityHorse":
		slot = slt + 2
	else:
		slot = slt
	
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
	
	name = options["Item Name"]
	lore = options["Item Lore"]
	container = options["Container Name"]

	canbreak = []
	if options["Can Break:"].upper() != "NONE":
		for a in options["Can Break:"].split(","):
			canbreak.append(TAG_String(a))

	canplace = []
	if options["Can Place On:"].upper() != "NONE":
		for a in options["Can Place On:"].split(","):
			canplace.append(TAG_String(a))

	if name == "None":
		name = ""
	if lore == "None":
		lore = ""
	if container == "None":
		container = ""
	if name != "":
		name = name.encode("unicode-escape")
		name = name.replace("|",sectional)
		name = name.decode("unicode-escape")
	if lore != "":
		lore = lore.encode("unicode-escape")
		lore = lore.replace("|",sectional)
		lore = lore.decode("unicode-escape")
	if container != "":
		container = container.encode("unicode-escape")
		container = container.replace("|",sectional)
		container = container.decode("unicode-escape")
		
	if potioneffect != -1:
		potion = TAG_Compound()
		potion["Amplifier"] = TAG_Byte(potionlevel-1)
		potion["Id"] = TAG_Byte(potioneffect)
		potion["Duration"] = TAG_Int(potionduration * 20)

	if op == "Set Dye Color Only":
		usedye = True
	if usedye:
		if dyestring[0] == "#":
			color = int(dyestring[1:7],16)
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
		for e in chunk.TileEntities if "Minecart" not in applytype and applytype != "EntityHorse" else chunk.Entities:
			if "Minecart" not in applytype and applytype != "EntityHorse":
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
			else:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
			if (x,y,z) in box:
				if e["id"].value in types.values():
					if "All" not in applytype:
						if e["id"].value == applytype:
							idtype = e["id"].value
						else:
							continue
					else:
						idtype = e["id"].value
					if op == "Find Items Matching Below":
						for i in e["Items"]:
							if slotmatch:
								if i["Slot"].value != slot:
									continue
							if namematch:
								if not checkname(i,name):
									continue
							if idmatch:
								if i["id"].value != id:
									continue
							if damagematch:
								if i["Damage"].value != damage:
									continue
							if countmatch:
								if i["Count"].value != count:
									continue
							print "Item",i["id"].value,":",i["Damage"].value,"found in a",e["id"].value,"at:",x, y, z,"in slot:",i["Slot"].value
						continue
					if op == "Fill Container":
						if "Items" in e:
							del e["Items"]
						e["Items"] = TAG_List()
						for c in xrange(capacities[idtype]):
							if e["id"].value == "EntityHorse":
								c += 2
							i = TAG_Compound()
							if shortVal:
								i["id"] = TAG_Short(id)
							else:
								i["id"] = TAG_String(id)
							i["Damage"] = TAG_Short(damage)
							i["Count"] = TAG_Byte(count)
							i["Slot"] = TAG_Byte(c)
							if enchantment >= 0 or (potioneffect != -1 and (id == 373 or "potion" in id)) or repair != -1 or usedye or name != "" or lore != "" or unbreakable:
								i["tag"] = TAG_Compound()
							if unbreakable:
								i["tag"]["Unbreakable"] = TAG_Byte(unbreakable)
							if enchantment >= 0:
								i["tag"]["ench"] = TAG_List()
								i["tag"]["ench"].append(ench)
							if potioneffect != -1 and id == 373:
								i["tag"]["CustomPotionEffects"] = TAG_List()
								i["tag"]["CustomPotionEffects"].append(potion)
							if repair != -1:
								i["tag"]["RepairCost"] = TAG_Int(repair)

							if usedye or name != "" or lore != "":
								i["tag"]["display"] = TAG_Compound()
								if usedye:
									i["tag"]["display"]["color"] = TAG_Int(color)
								if name != "":
									i["tag"]["display"]["Name"] = TAG_String(name)
								if lore != "":
									i["tag"]["display"]["Lore"] = TAG_List()
									i["tag"]["display"]["Lore"].append(TAG_String(lore))
							e["Items"].append(i)
							if container != "":
								e["CustomName"] = TAG_String(container)
						chunk.dirty = True
						continue
					if "Items" not in e:
						continue
					if op == "Empty Container":
						del e["Items"]
						e["Items"] = TAG_List()
						chunk.dirty = True
						continue
					elif op == "Add Item to Slot":
						for i in e["Items"]:
							if "Slot" in i:
								if i["Slot"].value == slot:
									if shortVal:
										i["id"] = TAG_Short(id)
									else:
										i["id"] = TAG_String(id)
									i["Damage"] = TAG_Short(damage)
									i["Count"] = TAG_Byte(count)
									if enchantment >= 0 or (potioneffect != -1 and (id == 373 or "potion" in id)) or repair != -1 or usedye or name != "" or lore != "" or unbreakable:
										i["tag"] = TAG_Compound()
									if unbreakable:
										i["tag"]["Unbreakable"] = TAG_Byte(unbreakable)
									if enchantment >= 0:
										i["tag"]["ench"] = TAG_List()
										i["tag"]["ench"].append(ench)
									if potioneffect != -1 and id == 373:
										i["tag"]["CustomPotionEffects"] = TAG_List()
										i["tag"]["CustomPotionEffects"].append(potion)
									if repair != -1:
										i["tag"]["RepairCost"] = TAG_Int(repair)

									if usedye or name != "" or lore != "":
										i["tag"]["display"] = TAG_Compound()
										if usedye:
											i["tag"]["display"]["color"] = TAG_Int(color)
										if name != "":
											i["tag"]["display"]["Name"] = TAG_String(name)
										if lore != "":
											i["tag"]["display"]["Lore"] = TAG_List()
											i["tag"]["display"]["Lore"].append(TAG_String(lore))
									chunk.dirty = True
									break
						else:
							i = TAG_Compound()
							if shortVal:
								i["id"] = TAG_Short(id)
							else:
								i["id"] = TAG_String(id)
							i["Damage"] = TAG_Short(damage)
							i["Count"] = TAG_Byte(count)
							i["Slot"] = TAG_Byte(slot)
							if enchantment >= 0 or (potioneffect != -1 and (id == 373 or "potion" in id)) or repair != -1 or usedye or name != "" or lore != "" or unbreakable:
								i["tag"] = TAG_Compound()
							if unbreakable:
								i["tag"]["Unbreakable"] = TAG_Byte(unbreakable)
							if enchantment >= 0:
								i["tag"]["ench"] = TAG_List()
								i["tag"]["ench"].append(ench)
							if potioneffect != -1 and id == 373:
								i["tag"]["CustomPotionEffects"] = TAG_List()
								i["tag"]["CustomPotionEffects"].append(potion)
							if repair != -1:
								i["tag"]["RepairCost"] = TAG_Int(repair)

							if usedye or name != "" or lore != "":
								i["tag"]["display"] = TAG_Compound()
								if usedye:
									i["tag"]["display"]["color"] = TAG_Int(color)
								if name != "":
									i["tag"]["display"]["Name"] = TAG_String(name)
								if lore != "":
									i["tag"]["display"]["Lore"] = TAG_List()
									i["tag"]["display"]["Lore"].append(TAG_String(lore))
							e["Items"].append(i)
							chunk.dirty = True
					elif op == "Remove Container Name":
						if "CustomName" in e:
							del e["CustomName"]
							chunk.dirty = True
							continue
					elif op == "Set Container Name Only" and container != "":
						e["CustomName"] = TAG_String(container)
						chunk.dirty = True
						continue

					for i in [b for b in e["Items"]]:
						if slotmatch:
							if i["Slot"].value != slot:
								continue
						if namematch:
							if not checkname(i,name):
								continue
						if idmatch:
							if i["id"].value != id:
								continue
						if damagematch:
							if i["Damage"].value != damage:
								continue
						if countmatch:
							if i["Count"].value != count:
								continue

						if "Remove" in op:
							if op == "Remove Item":
								e["Items"].remove(i)
								chunk.dirty = True
								continue
							elif op == "Remove Repair Cost":
								if "tag" in i:
									if "RepairCost" in i["tag"]:
										del i["tag"]["RepairCost"]
										chunk.dirty = True
										continue
							elif op == "Remove Item Name":
								if "tag" in i:
									if "display" in i["tag"]:
										if "Name" in i["tag"]["display"]:
											del i["tag"]["display"]["Name"]
											chunk.dirty = True
											continue
							elif op == "Remove Item Lores":
								if "tag" in i:
									if "display" in i["tag"]:
										if "Lore" in i["tag"]["display"]:
											del i["tag"]["display"]["Lore"]
											chunk.dirty = True
											continue
							elif op == "Remove Enchants":
								if "tag" in i:
									if "ench" in i["tag"]:
										del i["tag"]["ench"]
										chunk.dirty = True
										continue
							elif op == "Remove Potion Effects":
								if "tag" in i:
									if "CustomPotionEffects" in i["tag"]:
										del i["tag"]["CustomPotionEffects"]
										chunk.dirty = True
										continue
										
							elif op == "Remove Attribute Modifiers":
								if "tag" in i:
									if "AttributeModifiers" in i["tag"]:
										del i["tag"]["AttributeModifiers"]
										chunk.dirty = True
										continue

						elif op == "Set All":
							if shortVal:
								i["id"] = TAG_Short(id)
							else:
								i["id"] = TAG_String(id)
							i["Damage"] = TAG_Short(damage)
							i["Count"] = TAG_Byte(count)
							if "tag" in i:
								del i["tag"]
							if enchantment >= 0 or (potioneffect != -1 and (id == 373 or "potion" in id)) or repair != -1 or usedye or name != "" or lore != "" or unbreakable:
								i["tag"] = TAG_Compound()
							if unbreakable:
								i["tag"]["Unbreakable"] = TAG_Byte(unbreakable)
							if enchantment >= 0:
								i["tag"]["ench"] = TAG_List()
								i["tag"]["ench"].append(ench)
							if potioneffect != -1 and id == 373:
								i["tag"]["CustomPotionEffects"] = TAG_List()
								i["tag"]["CustomPotionEffects"].append(potion)
							if repair != -1:
								i["tag"]["RepairCost"] = TAG_Int(repair)

							if usedye or name != "" or lore != "":
								i["tag"]["display"] = TAG_Compound()
								if usedye:
									i["tag"]["display"]["color"] = TAG_Int(color)
								if name != "":
									i["tag"]["display"]["Name"] = TAG_String(name)
								if lore != "":
									i["tag"]["display"]["Lore"] = TAG_List()
									i["tag"]["display"]["Lore"].append(TAG_String(lore))
							chunk.dirty = True

						else:
							if op == "Set ID, Damage, and Count Only":
								if shortVal:
									i["id"] = TAG_Short(id)
								else:
									i["id"] = TAG_String(id)
								i["Damage"] = TAG_Short(damage)
								i["Count"] = TAG_Byte(count)
								chunk.dirty = True
							else:
								if "id" in i:
									if op == "Add Enchantment Only" and enchantment >= 0:
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										if "ench" not in i["tag"]:
											i["tag"]["ench"] = TAG_List()
										i["tag"]["ench"].append(ench)
										chunk.dirty = True
									elif op == "Set Repair Cost Only" and repair != -1:
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										i["tag"]["RepairCost"] = TAG_Int(repair)
										chunk.dirty = True
									elif op == "Add Potion Effect Only":
										if potioneffect != -1 and (i["id"].value == 373 or "potion" in i["id"].value):
											if "tag" not in i:
												i["tag"] = TAG_Compound()
											if "CustomPotionEffects" not in i["tag"]:
												i["tag"]["CustomPotionEffects"] = TAG_List()
											i["tag"]["CustomPotionEffects"].append(potion)
											chunk.dirty = True
									elif op == "Set Item Name Only" and name != "":
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										if "display" not in i["tag"]:
											i["tag"]["display"] = TAG_Compound()
										if "Lore" not in i["tag"]["display"]:
											i["tag"]["display"]["Lore"] = TAG_List()
										i["tag"]["display"]["Name"] = TAG_String(name)
										chunk.dirty = True
									elif op == "Prefix Lore Only" and lore != "":
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										if "display" not in i["tag"]:
											i["tag"]["display"] = TAG_Compound()
										if "Lore" not in i["tag"]["display"]:
											i["tag"]["display"]["Lore"] = TAG_List()
										i["tag"]["display"]["Lore"].insert(0,TAG_String(lore))
										chunk.dirty = True
									elif op == "Add Item Lore Only" and lore != "":
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										if "display" not in i["tag"]:
											i["tag"]["display"] = TAG_Compound()
										if "Lore" not in i["tag"]["display"]:
											i["tag"]["display"]["Lore"] = TAG_List()
										i["tag"]["display"]["Lore"].append(TAG_String(lore))
										chunk.dirty = True
									elif op == "Set Dye Color Only" and usedye:
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										if "display" not in i["tag"]:
											i["tag"]["display"] = TAG_Compound()
										i["tag"]["display"]["color"] = TAG_Int(color)
										chunk.dirty = True
									elif op == "Set Unbreakability":
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										i["tag"]["Unbreakable"] = TAG_Byte(unbreakable)
										chunk.dirty = True
									elif op == "Set Breakable Block List":
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										i["tag"]["CanDestroy"] = TAG_List(canbreak)
										chunk.dirty = True
									elif op == "Append to Breakable Block List":
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										if "CanDestroy" in i["tag"]:
											for c in canbreak:
												i["tag"]["CanDestroy"].append(c)
										else:
											i["tag"]["CanDestroy"] = TAG_List(canbreak)
										chunk.dirty = True
									elif op == "Set Placeable Block List":
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										i["tag"]["CanPlaceOn"] = TAG_List(canplace)
										chunk.dirty = True
									elif op == "Append to Placeable Block List":
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										if "CanPlaceOn" in i["tag"]:
											for c in canplace:
												i["tag"]["CanPlaceOn"].append(c)
										else:
											i["tag"]["CanPlaceOn"] = TAG_List(canplace)
										chunk.dirty = True
									elif op == "Add or Edit Attribute Modifier":
										if "tag" not in i:
											i["tag"] = TAG_Compound()
										if "AttributeModifiers" not in i["tag"]:
											i["tag"]["AttributeModifiers"] = TAG_List()
										for a in i["tag"]["AttributeModifiers"]:
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
											i["tag"]["AttributeModifiers"].append(attrib)
										chunk.dirty = True
									elif op == "List Attributes in Console":
										if "tag" in i:
											if "AttributeModifiers" in i["tag"]:
												print "Attribute Modifiers in container slot",i["Slot"].value,"of",e["id"].value,"at",x,y,z,":"
												for m in i["tag"]["AttributeModifiers"]:
													print "Modifier:",m["Name"].value,", amount:",str(m["Amount"].value),", operation:",str(m["Operation"].value),","
													print "uuid:",uuid.UUID(int=(((m["UUIDMost"].value & 0xFFFFFFFFFFFFFFFF) << 64) | (m["UUIDLeast"].value& 0xFFFFFFFFFFFFFFFF))).hex
