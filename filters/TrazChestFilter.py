from pymclevel import TAG_Byte, TAG_Short
from pymclevel import TileEntity

displayName = "TrazLander's Chest Filter"

inputs = (
	("Operate On Chest",True),
	("Operate On Furnace",True),
	("Operate On Dispenser",True),
	("Operate On Dropper",True),
	("Operate On Hopper",True),
	("Operate On Brewing Stand",True),
	("Operate On Minecart Chests",True),
	("Find Item ID:",(0, -32768, 32767)),
	("Find Item Damage:",(0, -32768, 32767)),
	("Replace Item ID:",(0, -32768, 32767)),
	("Replace Item Damage:",(0, -32768, 32767)),
	("Replace Item Count:",(0, -128, 127)),
	)
	
def perform(level, box, options):
	findid = options["Find Item ID:"]
	finddamage = options["Find Item Damage:"]
	replaceid = options["Replace Item ID:"]
	replacedamage = options["Replace Item Damage:"]
	replacecount = options["Replace Item Count:"]
	entitytypes = []
	if options["Operate On Chest"]:
		entitytypes.append("Chest")
	if options["Operate On Furnace"]:
		entitytypes.append("Furnace")
	if options["Operate On Dispenser"]:
		entitytypes.append("Trap")
	if options["Operate On Dropper"]:
		entitytypes.append("Dropper")
	if options["Operate On Hopper"]:
		entitytypes.append("Hopper")
	if options["Operate On Brewing Stand"]:
		entitytypes.append("Cauldron")
	if options["Operate On Minecart Chests"]:
		entitytypes.append("MinecartChest")

	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
		
			if (x,y,z) in box:
				if e["id"].value in entitytypes:
					if "Items" in e:
						for item in e["Items"]:
							if item["id"].value == findid and item["Damage"].value == finddamage:
								item["id"] = TAG_Short(replaceid)
								item["Damage"] = TAG_Short(replacedamage)
								item["Count"] = TAG_Byte(replacecount)
								chunk.dirty = True
		if options["Operate On Minecart Chests"]:
			for e in chunk.Entities:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
			
				if (x,y,z) in box:
					if e["id"].value in entitytypes:
						if "Items" in e:
							for item in e["Items"]:
								if item["id"].value == findid and item["Damage"].value == finddamage:
									item["id"] = TAG_Short(replaceid)
									item["Damage"] = TAG_Short(replacedamage)
									item["Count"] = TAG_Byte(replacecount)
									chunk.dirty = True