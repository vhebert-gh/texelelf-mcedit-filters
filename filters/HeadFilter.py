from pymclevel import TAG_List, TAG_Byte, TAG_Int, TAG_Compound, TAG_Short, TAG_Double, TAG_String
from random import randrange

displayName = "Head Filter"

HeadVals = {
	"Skeleton":0,
	"Wither Skeleton":1,
	"Zombie":2,
	"Steve or Player":3,
	"Creeper":4,
	}
	
rotvals = {
	"South (Wall and Floor)": 0x8,
	"South-Southwest (Floor Only)": 0x9,
	"Southwest (Floor Only)": 0xA,
	"West-Southwest (Floor Only)":0xB,
	"West (Wall and Floor)":0xC,
	"West-Northwest (Floor Only)":0xD,
	"Northwest (Floor Only)":0xE,
	"North-Northwest (Floor Only)":0xF,
	"North (Wall and Floor)":0x0,
	"North-Northeast (Floor Only)":0x1,
	"Northeast (Floor Only)":0x2,
	"East-Northeast (Floor Only)":0x3,
	"East (Wall and Floor)":0x4,
	"East-Southeast (Floor Only)":0x5,
	"Southeast (Floor Only)":0x6,
	"South-Southeast (Floor Only)":0x7,
	}
	
rotoptions = (
	"South (Wall and Floor)",
	"South-Southwest (Floor Only)",
	"Southwest (Floor Only)",
	"West-Southwest (Floor Only)",
	"West (Wall and Floor)",
	"West-Northwest (Floor Only)",
	"Northwest (Floor Only)",
	"North-Northwest (Floor Only)",
	"North (Wall and Floor)",
	"North-Northeast (Floor Only)",
	"Northeast (Floor Only)",
	"East-Northeast (Floor Only)",
	"East (Wall and Floor)",
	"East-Southeast (Floor Only)",
	"Southeast (Floor Only)",
	"South-Southeast (Floor Only)"
	)

	
inputs = (
	("Operation:", ("Fill","Replace","Apply to Entities","Apply to Spawners")),
	("Use Player Head", False),
	("Check playernames against http://www.minecraft.net/skin/<playername>.png","label"),
	("Player name:","string"),
	("Head is mounted on wall",False),
	("Head Type:", ("Skeleton","Wither Skeleton","Zombie","Steve or Player","Creeper")),
	("Rotation:",rotoptions),
	("Randomize Rotation",False),
	)

def perform(level, box, options):

	NewTileEntities = []
	
	op = options["Operation:"]
	onwall = options["Head is mounted on wall"]
	useplayer = options["Use Player Head"]
	PlayerName = options["Player name:"]
	headtype = HeadVals[options["Head Type:"]]
	rot = rotvals[options["Rotation:"]]
	randrot = options["Randomize Rotation"]

	if onwall:
		if rot == 8:
			rot = 3
		elif rot == 12:
			rot = 4
		elif rot == 0:
			rot = 2
		elif rot == 4:
			rot = 5
		else:
			rot = 3
	if useplayer:
		headtype = 3

	for (chunk, slices, point) in level.getChunkSlices(box):
		if op == "Replace":
			for e in chunk.TileEntities:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if (x,y,z) in box:
					if e["id"].value == "Skull":
						e["SkullType"] = TAG_Byte(headtype)
						if useplayer:
							e["ExtraType"] = TAG_String(PlayerName)
						else:
							e["ExtraType"] = TAG_String()
						if onwall:
							level.setBlockDataAt(x, y, z, rot if not randrot else randrange(2,6,1))
							e["Rot"] = TAG_Byte(0)
						else:
							e["Rot"] = TAG_Byte(rot if not randrot else randrange(0,16,1))

							
						chunk.dirty = True
		elif op == "Fill":
			(cx,cz) = chunk.chunkPosition
			cposx = cx * 16
			cposz = cz * 16
			for y in range(box.miny,box.maxy,1):
				for x in range((cposx if (cposx > box.minx) else box.minx),(cposx+16 if ((cposx+16) < box.maxx) else box.maxx),1):
					for z in range((cposz if (cposz > box.minz) else box.minz),(cposz+16 if((cposz+16) < box.maxz) else box.maxz),1):
						e = TAG_Compound()
						e["id"] = TAG_String("Skull")
						e["x"] = TAG_Int(x)
						e["y"] = TAG_Int(y)
						e["z"] = TAG_Int(z)
						level.setBlockAt(x, y, z, 144)
						if onwall:
							level.setBlockDataAt(x, y, z, rot if not randrot else randrange(2,6,1))
							e["Rot"] = TAG_Byte(0)
						else:
							level.setBlockDataAt(x, y, z, 1)
							e["Rot"] = TAG_Byte(rot if not randrot else randrange(0,16,1))

						e["SkullType"] = TAG_Byte(headtype)
						if useplayer:
							e["ExtraType"] = TAG_String(PlayerName)
						else:
							e["ExtraType"] = TAG_String()
						chunk.TileEntities.append(e)
			chunk.dirty = True
		elif op == "Apply to Entities":
			for e in chunk.Entities:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
				
				if (x,y,z) in box:
					if "Health" in e:
						if "Equipment" not in e:
							e["Equipment"] = TAG_List()
							e["Equipment"].append(TAG_Compound())
							e["Equipment"].append(TAG_Compound())
							e["Equipment"].append(TAG_Compound())
							e["Equipment"].append(TAG_Compound())
							e["Equipment"].append(TAG_Compound())
						if len(e["Equipment"]) == 5:
							e["Equipment"][4]["id"] = TAG_String("minecraft:skull")
							e["Equipment"][4]["Damage"] = TAG_Short(headtype)
							e["Equipment"][4]["Count"] = TAG_Byte(0)
							if useplayer:
								if "tag" not in e["Equipment"][4]:
									e["Equipment"][4]["tag"] = TAG_Compound()
								e["Equipment"][4]["tag"]["SkullOwner"] = TAG_String(PlayerName)
							chunk.dirty = True

		elif op == "Apply to Spawners":
			for e in chunk.TileEntities:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if (x,y,z) in box:
					if e["id"].value == "MobSpawner":
						if "SpawnData" not in e:
							e["SpawnData"] = TAG_Compound()
						if "Equipment" not in e["SpawnData"]:
							e["SpawnData"]["Equipment"] = TAG_List()
							e["SpawnData"]["Equipment"].append(TAG_Compound())
							e["SpawnData"]["Equipment"].append(TAG_Compound())
							e["SpawnData"]["Equipment"].append(TAG_Compound())
							e["SpawnData"]["Equipment"].append(TAG_Compound())
							e["SpawnData"]["Equipment"].append(TAG_Compound())
						if len(e["SpawnData"]["Equipment"]) == 5:
							e["SpawnData"]["Equipment"][4]["id"] = TAG_String("minecraft:skull")
							e["SpawnData"]["Equipment"][4]["Damage"] = TAG_Short(headtype)
							e["SpawnData"]["Equipment"][4]["Count"] = TAG_Byte(0)
							if useplayer:
								if "tag" not in e["SpawnData"]["Equipment"][4]:
									e["SpawnData"]["Equipment"][4]["tag"] = TAG_Compound()
								e["SpawnData"]["Equipment"][4]["tag"]["SkullOwner"] = TAG_String(PlayerName)
							chunk.dirty = True