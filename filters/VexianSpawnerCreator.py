# Feel free to modify and use this filter however you wish. If you do,
# please give credit to SethBling.
# http://youtube.com/SethBling
#
# and also texelelf
# http://youtube.com/texelelf

from copy import deepcopy
from random import randrange
from pymclevel.materials import alphaMaterials
from pymclevel import TAG_Compound
from pymclevel import TAG_Int
from pymclevel import TAG_Short
from pymclevel import TAG_Byte
from pymclevel import TAG_String
from pymclevel import TAG_Float
from pymclevel import TAG_Double
from pymclevel import TAG_List
from pymclevel import Entity, TileEntity

displayName = "The Vexian Spawner Creator"

minecart_list = ("Normal","Chest Minecart","Furnace Minecart")
minecart_vals = {
	"Normal":0,
	"Chest Minecart":1,
	"Furnace Minecart":2
	}

entity_list = (
	"Arrow",
	"Snowball",
	"Fireball",
	"SmallFireball",
	"WitherSkull",
	"ThrownEnderpearl",
	"ThrownPotion",
	"ThrownExpBottle",
	"Item",
	"XPOrb",
	"EyeOfEnderSignal",
	"EnderCrystal",
	"Minecart",
	"Boat",
	"PrimedTnt",
	"FallingSand"
	)

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
	
splash_potions = (
	"None (Water bottle)",
	"Instant Health",
	"Instant Health II",
	"Instant Damage",
	"Instant Damage II",
	"Regeneration (0:33)",
	"Regeneration (1:30)",
	"Regeneration II (0:16)",
	"Regeneration II (0:45)",
	"Strength (2:15)",
	"Strength (6:00)",
	"Strength II (1:07)",
	"Strength II (3:00)",
	"Speed (2:15)",
	"Speed (6:00)",
	"Speed II (1:07)",
	"Speed II (3:00)",
	"Fire Resist (2:15)",
	"Fire Resist (6:00)",
	"Poison (0:33)",
	"Poison (1:30)",
	"Poison II (0:16)",
	"Poison II (0:45)",
	"Slowness (1:07)",
	"Slowness (3:00)",
	"Weakness (1:07)",
	"Weakness (3:00)",
	)
potion_list = {
	"None (Water bottle)":0,
	"Strength II (3:00)": 32761,
	"Poison II (0:45)": 32756,
	"Speed II (3:00)": 32754,
	"Regeneration II (0:45)": 32753,
	"Slowness (3:00)": 32762,
	"Strength (6:00)": 32729,
	"Weakness (3:00)": 32760,
	"Poison (1:30)": 32724,
	"Fire Resist (6:00)": 32755,
	"Speed (6:00)": 32722,
	"Regeneration (1:30)": 32721,
	"Strength II (1:07)": 32697,
	"Poison II (0:16)": 32692,
	"Speed II (1:07)": 32690,
	"Regeneration II (0:16)": 32689,
	"Slowness (1:07)": 32698,
	"Strength (2:15)": 32665,
	"Weakness (1:07)": 32696,
	"Poison (0:33)": 32660,
	"Fire Resist (2:15)": 32691,
	"Speed (2:15)": 32658,
	"Regeneration (0:33)": 32657,
	"Instant Health": 32725,
	"Instant Health II": 32757,
	"Instant Damage": 32732,
	"Instant Damage II": 32764
	}
	
potion_effects_vals = {
	"None": -1,
	"Strength": 5,
	"Jump Boost": 8,
	"Regeneration": 10,
	"Fire Resistance": 12,
	"Water Breathing": 13,
	"Resistance": 11,
	"Weakness": 18,
	"Poison": 19,
	"Speed": 1,
	"Slowness": 2,
	"Haste": 3,
	"Mining Fatigue": 4,
	"Nausea": 9,
	"Blindness": 15,
	"Hunger": 17,
	"Invisibility": 14,
	"Night Vision": 16,
	}
	
potion_effects = (
	"None",
	"Strength",
	"Jump Boost",
	"Regeneration",
	"Fire Resistance",
	"Water Breathing",
	"Resistance",
	"Weakness",
	"Poison",
	"Speed",
	"Slowness",
	"Haste",
	"Mining Fatigue",
	"Nausea",
	"Blindness",
	"Hunger",
	"Invisibility",
	"Night Vision",
	)
	
noop = -1337
fnoop = -1337.0
inputs = (
	("Operation:",("Fill","Random Fill Number","Random Fill Percent","Grid Fill","Add and Replace Properties","Clear All Properties","Set Item in Slot","Add Enchant (Slot or Spawner)", "Output Properties to Console")),
	("Number or Percentage/Grid Size",10.0),
	("Entity Type",entity_list),
	("Block Replace Mode", ("None","Replace","Do Not Replace")),
	("Block to Replace", alphaMaterials.Air),
	("Ticks Until Spawn", (-32768,noop,32767)),
	("Min Ticks Between Spawns",noop),
	("Ticks Between Spawns",noop),
	("Max Number of Entities Per Spawn", (-32768,1,32767)),
	("Positioning Mode",("Ignore Values","Relative","Absolute")),
	("PosX",fnoop),
	("PosY",fnoop),
	("PosZ",fnoop),
	("VelocityX", fnoop),
	("VelocityY", fnoop),
	("VelocityZ", fnoop),
	
	("Arrow recoverable", False),
	("Base Potion Type",splash_potions),
	("Additional Potion Effects",potion_effects),
	("Potion Level",(1,-128, 127)),
	("Potion Duration in Seconds",(0, 0, 100000000)),
	("Amount of XP per orb", (noop,-32768,32767)),
	
	("Fuse Length (TNT)",(70,0,127)),
	("Falling Block ID", alphaMaterials.Air),
	("Num ticks block has been falling", noop),
	("Falling block drops item", False),
	("Minecart Type", minecart_list),
	("Furnace Minecart Fuel", (noop,-32768,32767)),
	("Item Slot #", (0,0,127)),
	("Item ID", (noop,-32768,32767)),
	("Item Damage",(0,-32768,32767)),
	("Number of Items",(1,-128,127)),
	("Item Age",(noop,-32768,32767)),
	("Item Enchant", enchantments),
	("Item Enchant Level", (1,-32768,32767)),
	
	("Fire", (noop,-32768,32767)),
	("FallDistance", noop),
)


def perform(level, box, options):
	doreplace = options["Block Replace Mode"]
	blockreplace = options["Block to Replace"]
	delay = options["Ticks Until Spawn"]
	spawndelay = options["Ticks Between Spawns"]
	minspawndelay = options["Min Ticks Between Spawns"]
	numspawn = options["Max Number of Entities Per Spawn"]
	posmode = options["Positioning Mode"]
	posx = options["PosX"]
	posy = options["PosY"]
	posz = options["PosZ"]
	vx = options["VelocityX"]
	vy = options["VelocityY"]
	vz = options["VelocityZ"]
	fire = options["Fire"]
	fall = options["FallDistance"]
	
	recover = options["Arrow recoverable"]
	fuse = options["Fuse Length (TNT)"]
	itemslot = options["Item Slot #"]
	itemid = options["Item ID"]
	itemdamage = options["Item Damage"]
	numitems = options["Number of Items"]
	itemage = options["Item Age"]
	enchant = options["Item Enchant"]
	enchantlevel = options["Item Enchant Level"]

	fallid = options["Falling Block ID"]
	fallticks = options["Num ticks block has been falling"]
	dodrop = options["Falling block drops item"]
	carttype = options["Minecart Type"]
	cartfuel = options["Furnace Minecart Fuel"]
	potionvalue = options["Base Potion Type"]
	addpotion = potion_effects_vals[options["Additional Potion Effects"]]
	addpotionlevel = options["Potion Level"]
	addpotionlength = options["Potion Duration in Seconds"]
	xpvalue = options["Amount of XP per orb"]


	filltype = options["Operation:"]
	percentage = options["Number or Percentage/Grid Size"]
	mob = options["Entity Type"]

	height = abs(box.maxy) - abs(box.miny)
	if filltype == "Random Fill Number":
		if (int(percentage) >= ((box.maxx-box.minx)*(box.maxz-box.minz)*(box.maxy-box.miny))):
			filltype = "Fill"
		count = int(percentage)
	elif filltype == "Grid Fill":
		count = int(percentage)+1
		
	if doreplace == "None":
		doreplace = False
		donotreplace = False
	elif doreplace == "Replace":
		doreplace = True
		donotreplace = False
	elif doreplace == "Do Not Replace":
		doreplace = True
		donotreplace = True
	
	
	spawner_save = TileEntity.Create("MobSpawner")
	if minspawndelay != noop:
		if minspawndelay > 32767:
			minspawndelay = 32767
		elif minspawndelay < 0:
			minspawndelay = 0
	if spawndelay != noop:
		if spawndelay > 32767:
			spawndelay = 32767
		elif spawndelay < 1:
			spawndelay = 1
		spawner_save["MinSpawnDelay"] = TAG_Short(minspawndelay if (minspawndelay != noop and minspawndelay < spawndelay) else spawndelay)
		spawner_save["MaxSpawnDelay"] = TAG_Short(spawndelay)
	else:
		spawner_save["MinSpawnDelay"] = TAG_Short(200)
		spawner_save["MaxSpawnDelay"] = TAG_Short(800)

	spawner_save["SpawnCount"] = TAG_Short(numspawn)

	spawner_save["MaxNearbyEntities"] = TAG_Short(1)
	spawner_save["RequiredPlayerRange"] = TAG_Short(10)
	
	if delay != noop:
		spawner_save["Delay"] = TAG_Short(delay)
	else:
		spawner_save["Delay"] = TAG_Short(120)


	spawner_save["EntityId"] = TAG_String(mob)
	spawner_save["SpawnData"] = TAG_Compound()

	entity = Entity.Create(mob)
	entity["EntityId"] = TAG_String(mob)
	if posmode == "Absolute" and (posx == fnoop or posy == fnoop or posz == fnoop):
		posmode = "Relative"
	posx = posx if posx != fnoop else 0.0
	posy = posy if posy != fnoop else 0.0
	posz = posz if posz != fnoop else 0.0
	if posmode == "Absolute":
		Entity.setpos(entity,(posx,posy,posz))
	elif posmode == "Ignore Values":
		del entity["Pos"]
	if vx != fnoop or vy != fnoop or vz != fnoop:
		entity["Motion"] = TAG_List()
		entity["Motion"].append(TAG_Double(0.0))
		entity["Motion"].append(TAG_Double(0.0))
		entity["Motion"].append(TAG_Double(0.0))
	if vx != fnoop:
		entity["Motion"][0] = TAG_Double(vx)
	if vy != fnoop:
		entity["Motion"][1] = TAG_Double(vy)
	if vz != fnoop:
		entity["Motion"][2] = TAG_Double(vz)

		
	if mob == "Arrow" and recover:
		entity["pickup"] = TAG_Byte(recover)
	
	if "Fireball" in mob:
		if posmode == "Relative" or posmode == "Absolute":
			spawner_save["SpawnCount"] = TAG_Short(1)
		if vx == fnoop and vy == fnoop and vz == fnoop:
			entity["Motion"] = TAG_List()
			entity["Motion"].append(TAG_Double(0.0))
			entity["Motion"].append(TAG_Double(0.0))
			entity["Motion"].append(TAG_Double(0.0))
		
		entity["direction"] = TAG_List()
		entity["direction"].append(entity["Motion"][0])
		entity["direction"].append(entity["Motion"][1])
		entity["direction"].append(entity["Motion"][2])
		
		entity["inGround"] = TAG_Byte(0)
		entity["inTile"] = TAG_Byte(0)
		entity["FallDistance"] = TAG_Float(0.0)
		entity["Fire"] = TAG_Short(20)
		entity["xTile"] = TAG_Short(-1)
		entity["yTile"] = TAG_Short(-1)
		entity["zTile"] = TAG_Short(-1)
		entity["OnGround"] = TAG_Byte(0)
		
	if mob == "PrimedTnt":
		entity["Fuse"] = TAG_Byte(fuse)

	if mob == "ThrownPotion":
		entity["potionValue"] = TAG_Int(potion_list[potionvalue])
		entity["Potion"] = TAG_Compound()
		entity["Potion"]["id"] = TAG_Short(373)
		entity["Potion"]["Damage"] = TAG_Short(potion_list[potionvalue])
		entity["Potion"]["Count"] = TAG_Byte(1)
		if addpotion != -1:
			entity["Potion"]["tag"] = TAG_Compound()
			entity["Potion"]["tag"]["CustomPotionEffects"] = TAG_List()
			potion = TAG_Compound()
			potion["Id"] = TAG_Byte(addpotion)
			potion["Amplifier"] = TAG_Byte(addpotionlevel-1)
			potion["Duration"] = addpotionlength * 20
			entity["Potion"]["tag"]["CustomPotionEffects"].append(potion)

	if mob == "Item":
		if itemid != noop:
			entity["Age"] = TAG_Short(itemage)
			entity["Item"] = TAG_Compound()
			item = TAG_Compound()
			item["id"] = TAG_Short(itemid)
			item["Count"] = TAG_Byte(numitems)

			item["Damage"] = TAG_Short(itemdamage)
			if enchant != "None" or addpotion != -1:
				item["tag"] = TAG_Compound()
			if enchant != "None":
				item["tag"]["ench"] = TAG_List()
				ench = TAG_Compound()
				ench["id"] = TAG_Short(enchantment_vals[enchant])
				ench["lvl"] = TAG_Short(enchantlevel)
				item["tag"]["ench"].append(ench)
			if addpotion != -1:
				item["tag"]["CustomPotionEffects"] = TAG_List()
				potion = TAG_Compound()
				potion["Id"] = TAG_Byte(addpotion)
				potion["Amplifier"] = TAG_Byte(addpotionlevel-1)
				potion["Duration"] = addpotionlength * 20
				item["tag"]["CustomPotionEffects"].append(potion)
			entity["Item"] = item
		
	if mob == "XPOrb":
		if xpvalue != noop:
			entity["Value"] = TAG_Short(xpvalue)
			
	if mob == "Minecart" or (filltype == "Set Item in Slot" or filltype == "Add Enchant (Slot or Spawner)"):
		if mob == "Minecart":
			entity["Type"] = TAG_Int(minecart_vals[carttype])
		if carttype == "Furnace Minecart":
			entity["Fuel"] = TAG_Short(cartfuel)
		elif carttype == "Chest Minecart" or (filltype == "Set Item in Slot" or filltype == "Add Enchant (Slot or Spawner)"):
			if itemid != noop:
				entity["Items"] = TAG_List()
				item = TAG_Compound()

				item["id"] = TAG_Short(itemid)
				item["Slot"] = TAG_Byte(itemslot)
				item["Count"] = TAG_Byte(numitems)
				item["Damage"] = TAG_Short(itemdamage)
				if enchant != "None" or addpotion != -1:
					item["tag"] = TAG_Compound()
				if enchant != "None":
					item["tag"]["ench"] = TAG_List()
					ench = TAG_Compound()
					ench["id"] = TAG_Short(enchantment_vals[enchant])

					ench["lvl"] = TAG_Short(enchantlevel)
					item["tag"]["ench"].append(ench)
				if addpotion != -1:
					item["tag"]["CustomPotionEffects"] = TAG_List()
					potion = TAG_Compound()
					potion["Id"] = TAG_Byte(addpotion)
					potion["Amplifier"] = TAG_Byte(addpotionlevel-1)
					potion["Duration"] = addpotionlength * 20
					item["tag"]["CustomPotionEffects"].append(potion)
				entity["Items"].append(item)
		
	if mob == "FallingSand":
		posx += 0.5
		posz += 0.5
		entity["Tile"] = TAG_Byte(fallid.ID)
		entity["Data"] = TAG_Byte(fallid.blockData)
		if fallticks != noop:
			entity["Time"] = TAG_Byte(fallticks)
		else:
			entity["Time"] = TAG_Byte(1)
		entity["DropItem"] = TAG_Byte(dodrop)
		
	if fire != noop:
		entity["Fire"] = TAG_Short(fire)
	if fall != noop:
		entity["FallDistance"] = TAG_Float(fall)

	del entity["id"]
	entity_save = deepcopy(entity)

	entitiesToRemove = []
	overlappingTileEntities = []
	chunkEntityCoords = []
	originalEntityList = []
	addEntityList = []
	
	def SetBlock(bx,by,bz,outer=False):
		if (bx,by,bz) in chunkEntityCoords:
			overlappingTileEntities.append((bx,by,bz))
		entity = deepcopy(entity_save)
		spawner = deepcopy(spawner_save)
		level.setBlockAt(bx, by, bz, 52)
		TileEntity.setpos(spawner, (bx, by, bz))
		if posmode == "Relative":
			Entity.setpos(entity,(bx+posx,by+posy,bz+posz))
		spawner["SpawnData"] = entity
		if not outer:
			chunk.TileEntities.append(spawner)
		else:
			addEntityList.append(spawner)

	randnumlist = []	
	for (chunk, slices, point) in level.getChunkSlices(box):
		chunkEntityCoords = []
		(cx,cz) = chunk.chunkPosition
		cposx = cx * 16
		cposz = cz * 16
		if "Fill" in filltype:
			for entity in chunk.TileEntities:
				ex = entity["x"].value
				ey = entity["y"].value
				ez = entity["z"].value
				if ex >= box.minx and ex < box.maxx and ey >= box.miny and ey < box.maxy and ez >= box.minz and ez < box.maxz:
					chunkEntityCoords.append((ex,ey,ez))
					originalEntityList.append(entity)
			if filltype == "Fill":
				for y in range(box.miny,box.maxy,1):
					for x in range((cposx if (cposx > box.minx) else box.minx),(cposx+16 if ((cposx+16) < box.maxx) else box.maxx),1):
						for z in range((cposz if (cposz > box.minz) else box.minz),(cposz+16 if((cposz+16) < box.maxz) else box.maxz),1):
							if not doreplace:
								SetBlock(x,y,z)
							elif doreplace and not donotreplace and level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData:
								SetBlock(x,y,z)
							elif donotreplace and not (level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData):
								SetBlock(x,y,z)
			elif filltype == "Grid Fill":
				for y in range(box.miny,box.maxy,count):
					for x in range(cposx+((box.minx-cposx)%count),cposx+16,count):
						for z in range(cposz+((box.minz-cposz)%count),cposz+16,count):
							if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
								if not doreplace:
									SetBlock(x,y,z)
								elif doreplace and not donotreplace and level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData:
									SetBlock(x,y,z)
								elif donotreplace and not (level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData):
									SetBlock(x,y,z)

			for oldentity in originalEntityList:
				ox = oldentity["x"].value
				oy = oldentity["y"].value
				oz = oldentity["z"].value
				if (ox,oy,oz) in overlappingTileEntities:
					entitiesToRemove.append((chunk, oldentity))
			
			chunk.dirty = True
			
			overlappingTileEntities[:] = []
			originalEntityList[:] = []
			chunkEntityCoords[:] = []
		else:
			for entity in chunk.TileEntities:
				x = entity["x"].value
				y = entity["y"].value
				z = entity["z"].value
				if "id" not in entity:
					continue
				if entity["id"].value != "MobSpawner":
					continue
				if "EntityId" not in entity:
					print "WARNING: Malformed mobspawner at", x, y, z,".  Overwriting."
					entity["EntityId"] = entity_save["EntityId"]
				if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
					if filltype == "Clear All Properties":
						for a in entity.keys():
							if a != "id" and a != "x" and a != "y" and a != "z" and a != "EntityId":
								del entity[a]
					elif filltype == "Add and Replace Properties":
						if "Delay" in spawner_save:
							entity["Delay"] = spawner_save["Delay"]
						if "MinSpawnDelay" in spawner_save:
							entity["MinSpawnDelay"] = spawner_save["MinSpawnDelay"]
						if "MaxSpawnDelay" in spawner_save:
							entity["MaxSpawnDelay"] = spawner_save["MaxSpawnDelay"]
						if "SpawnCount" in spawner_save:
							entity["SpawnCount"] = spawner_save["SpawnCount"]
						if "SpawnData" in spawner_save:
							if "SpawnData" not in entity:
								entity["SpawnData"] = TAG_Compound()
								savedentity = deepcopy(entity_save)
								savedentity["EntityId"] = entity["EntityId"]
								if posmode == "Relative":
									Entity.setpos(savedentity,(x+posx,y+posy,z+posz))
								entity["SpawnData"] = savedentity
							else:
								for e in entity_save.keys():
									if e == "Pos":
										if posmode == "Relative":
											Entity.setpos(entity["SpawnData"],(x+posx,y+posy,z+posz))
										elif posmode == "Absolute":
											entity["SpawnData"]["Pos"] = entity_save["Pos"]
									else:
										entity["SpawnData"][e] = entity_save[e]
					elif filltype == "Set Item in Slot" and entity["EntityId"].value == "Minecart":
						if "SpawnData" not in entity:
							entity["SpawnData"] = TAG_Compound()
							savedentity = deepcopy(entity_save)
							savedentity["EntityId"] = entity["EntityId"]
							if posmode == "Relative":
								Entity.setpos(savedentity,(x+posx,y+posy,z+posz))
							entity["SpawnData"] = savedentity
						else:
							if "Items" in entity_save and entity["SpawnData"]["Type"].value == 1:
								if "Items" not in entity["SpawnData"]:
									entity["SpawnData"]["Items"] = TAG_List()
									entity["SpawnData"]["Items"].append(entity_save["Items"][0])
								else:
									for it,trash in enumerate(entity["SpawnData"]["Items"]):
										if entity["SpawnData"]["Items"][it]["Slot"].value == entity_save["Items"][0]["Slot"].value:
											entity["SpawnData"]["Items"][it]["Damage"] = entity_save["Items"][0]["Damage"]
											entity["SpawnData"]["Items"][it]["Count"] = entity_save["Items"][0]["Count"]
											entity["SpawnData"]["Items"][it]["id"] = entity_save["Items"][0]["id"]
											if "tag" in entity["SpawnData"]["Items"][it]:
												if "tag" in entity_save["Items"][0]:
													if "ench" in entity["SpawnData"]["Items"][it]["tag"]:
														if "ench" not in entity_save["Items"][0]["tag"]:
															print "ERROR: Incorrectly built item entity!"
														else:
															del entity["SpawnData"]["Items"][it]["tag"]["ench"]
															entity["SpawnData"]["Items"][it]["tag"]["ench"] = TAG_List()
															entity["SpawnData"]["Items"][it]["tag"]["ench"].append(entity_save["Items"][0]["tag"]["ench"][0])
													else:
														entity["SpawnData"]["Items"][it]["tag"]["ench"] = TAG_List()
														entity["SpawnData"]["Items"][it]["tag"]["ench"].append(entity_save["Items"][0]["tag"]["ench"][0])
												else:
													del entity["SpawnData"]["Items"][it]["tag"]
											elif "tag" in entity_save["Items"][0]:
												entity["SpawnData"]["Items"][it]["tag"] = TAG_Compound()
												entity["SpawnData"]["Items"][it]["tag"] = entity_save["Items"][0]["tag"]
											break
									else:
										entity["SpawnData"]["Items"].append(entity_save["Items"][0])
					elif filltype == "Add Enchant (Slot or Spawner)":
						if entity["EntityId"].value == "Minecart" or entity["EntityId"].value == "Item":
							if "SpawnData" not in entity:
								if entity["EntityId"].value == "Minecart":
									entity["SpawnData"] = TAG_Compound()
									savedentity = deepcopy(entity_save)
									savedentity["EntityId"] = entity["EntityId"]
									if posmode == "Relative":
										Entity.setpos(savedentity,(x+posx,y+posy,z+posz))
									entity["SpawnData"] = savedentity
								else:
									entity["SpawnData"] = TAG_Compound()
									savedentity = deepcopy(entity_save)
									savedentity["EntityId"] = entity["EntityId"]
									if posmode == "Relative":
										Entity.setpos(savedentity,(x+posx,y+posy,z+posz))
									del savedentity["Items"]
									savedentity["Item"] = TAG_Compound()
									savedentity["Item"] = entity_save["Items"][0]
									entity["SpawnData"] = savedentity
							else:
								if "Items" in entity_save:
									if "tag" in entity_save["Items"][0]:
										if "ench" in entity_save["Items"][0]["tag"]:
											if entity["EntityId"].value == "Minecart" and entity["SpawnData"]["Type"].value == 1:
												if "Items" not in entity["SpawnData"]:
													entity["SpawnData"]["Items"] = TAG_List()
													entity["SpawnData"]["Items"].append(entity_save["Items"][0])
												else:
													for it,trash in enumerate(entity["SpawnData"]["Items"]):
														if entity["SpawnData"]["Items"][it]["Slot"].value == entity_save["Items"][0]["Slot"].value:
															if "tag" in entity["SpawnData"]["Items"][it]:
																if "ench" in entity["SpawnData"]["Items"][it]["tag"]:
																		entity["SpawnData"]["Items"][it]["tag"]["ench"].append(entity_save["Items"][0]["tag"]["ench"][0])
																else:
																	entity["SpawnData"]["Items"][it]["tag"]["ench"] = TAG_List()
																	entity["SpawnData"]["Items"][it]["tag"]["ench"].append(entity_save["Items"][0]["tag"]["ench"][0])
															else:
																entity["SpawnData"]["Items"][it]["tag"] = TAG_Compound()
																entity["SpawnData"]["Items"][it]["tag"]["ench"] = TAG_List()
																entity["SpawnData"]["Items"][it]["tag"]["ench"].append(entity_save["Items"][0]["tag"]["ench"][0])
											else:
												if "Item" not in entity["SpawnData"]:
													entity["SpawnData"]["Item"] = TAG_Compound()
													entity["SpawnData"]["Item"] = entity_save["Items"][0]
												else:
													if "tag" in entity["SpawnData"]["Item"]:
														if "ench" in entity["SpawnData"]["Item"]["tag"]:
															entity["SpawnData"]["Item"]["tag"]["ench"].append(entity_save["Items"][0]["tag"]["ench"][0])
														else:
															entity["SpawnData"]["Item"]["tag"]["ench"] = TAG_List()
															entity["SpawnData"]["Item"]["tag"]["ench"].append(entity_save["Items"][0]["tag"]["ench"][0])
													else:
														entity["SpawnData"]["Item"]["tag"] = TAG_Compound()
														entity["SpawnData"]["Item"]["tag"]["ench"] = TAG_List()
														entity["SpawnData"]["Item"]["tag"]["ench"].append(entity_save["Items"][0]["tag"]["ench"][0])

					elif filltype == "Output Properties to Console":
						print entity
			chunk.dirty = True


	if filltype == "Random Fill Number" or filltype == "Random Fill Percent":
		numblocks = int((box.maxy-box.miny)*(box.maxx-box.minx)*(box.maxz-box.minz))
		if filltype == "Random Fill Percent":
				count = int((box.maxy-box.miny)*(box.maxx-box.minx)*(box.maxz-box.minz) * (percentage*.01))
		itr = 0
		while itr < (count if count <= numblocks else numblocks) and itr < numblocks:
			numtries = 0
			while True:
				y = randrange(box.miny,box.maxy,1)
				x = randrange(box.minx,box.maxx,1)
				z = randrange(box.minz,box.maxz,1)
				if (x,y,z) not in randnumlist:
					randnumlist.append((x,y,z))
					break
				else:
					numtries = numtries + 1
					if numtries > numblocks:
						itr = numblocks
						break
			if not doreplace:
				if level.tileEntityAt(x,y,z):
					entitiesToRemove.append(level.tileEntityAt(x,y,z))
				SetBlock(x,y,z,True)
				itr = itr + 1
			elif doreplace and not donotreplace and level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData:
				if level.tileEntityAt(x,y,z):
					entitiesToRemove.append(level.tileEntityAt(x,y,z))
				SetBlock(x,y,z,True)
				itr = itr + 1
			elif donotreplace and not (level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData):
				if level.tileEntityAt(x,y,z):
					entitiesToRemove.append(level.tileEntityAt(x,y,z))
				SetBlock(x,y,z,True)
				itr = itr + 1
		for (chunk, slices, point) in level.getChunkSlices(box):
			(cx,cz) = chunk.chunkPosition
			cposx = cx * 16
			cposz = cz * 16
			for entity in addEntityList:
				if ((cposx <= entity["x"].value < (cposx + 16)) and (cposz <= entity["z"].value < (cposz + 16))):
					chunk.TileEntities.append(entity)
		level.markDirtyBox(box)
					
	if "Fill" in filltype:
		for (chunk, entity) in entitiesToRemove:
			chunk.TileEntities.remove(entity)

			
