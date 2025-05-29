from pymclevel import TAG_List, TAG_Compound, TAG_String, TAG_Double, TAG_Byte, TAG_Int, TAG_Long

displayName = "Attribute Filter"

attributes =(	"None",
				"generic.maxHealth","generic.followRange","generic.knockbackResistance",
				"generic.movementSpeed","generic.attackDamage","horse.jumpStrength","zombie.spawnReinforcements"
			)

inputs = (
	("Apply to:",("Mobs","Item Entities")),
	("Pre-defined Attributes",attributes),
	("Custom Attribute Name",("string","val=")),
	("Name",("string","val=")),
	("Amount or Base",0.0),
	("Operation",(0,-2147483648,2147483647)),
	("Use 0 below to not include UUID values","label"),
	("Least-Significant UUID value:",(0,-9223372036854775808,9223372036854775807)),
	("Most-Significant UUID value:",(0,-9223372036854775808,9223372036854775807)),
	)

def perform(level, box, options):
	apply = options["Apply to:"]
	predef = options["Pre-defined Attributes"]
	custom = options["Custom Attribute Name"]
	name = options["Name"]
	amount = options["Amount or Base"]
	oper = options["Operation"]
	least = options["Least-Significant UUID value:"]
	most = options["Most-Significant UUID value:"]
	
	if predef != "None":
		attr = predef
	else:
		attr = custom

	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.Entities:
			x = e["Pos"][0].value
			y = e["Pos"][1].value
			z = e["Pos"][2].value
			if (x,y,z) in box:
				if apply == "Item Entities":
					if e["id"].value == "Item":
						if "Item" not in e:
							print "ERROR!  Malformed Item entity at",x,y,z
							continue
						if "tag" not in e["Item"]:
							e["Item"]["tag"] = TAG_Compound()
						if "AttributeModifiers" not in e["Item"]["tag"]:
							e["Item"]["tag"]["AttributeModifiers"] = TAG_List()
						edited = False
						for a in e["Item"]["tag"]["AttributeModifiers"]:
							if a["AttributeName"].value == attr:
								a["Amount"] = TAG_Double(amount)
								a["Operation"] = TAG_Int(oper)
								edited = True
						if not edited:
							attrib = TAG_Compound()
							attrib["Name"] = TAG_String(name)
							attrib["AttributeName"] = TAG_String(attr)
							attrib["Amount"] = TAG_Double(amount)
							attrib["Operation"] = TAG_Int(oper)
							if least != 0:
								attrib["UUIDLeast"] = TAG_Long(least)
							if most != 0:
								attrib["UUIDMost"] = TAG_Long(most)
							e["Item"]["tag"]["AttributeModifiers"].append(attrib)

						chunk.dirty = True
				else:
					if "Health" in e:
						if "Attributes" not in e:
							e["Attributes"] = TAG_List()
						edited = False
						for a in e["Attributes"]:
							if a["Name"].value == attr:
								a["Base"] = TAG_Double(amount)
								edited = True
						if not edited:
							attrib = TAG_Compound()
							attrib["Name"] = TAG_String(attr)
							attrib["Base"] = TAG_Double(amount)
							if least != 0:
								attrib["UUIDLeast"] = TAG_Long(least)
							if most != 0:
								attrib["UUIDMost"] = TAG_Long(most)
							e["Attributes"].append(attrib)
						chunk.dirty = True
