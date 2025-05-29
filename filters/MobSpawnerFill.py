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

displayName = "All-Purpose Mob Spawner Tool"

monsters = (
	"Bat",
	"Blaze",
	"CaveSpider",
	"Chicken",
	"Cow",
	"Creeper",
	"EnderDragon",
	"Enderman",
	"Ghast",
	"Giant",
	"LavaSlime",
	"MushroomCow",
	"Pig",
	"PigZombie",
	"Silverfish",
	"Sheep",
	"Skeleton",
	"Slime",
	"SnowMan",
	"Spider",
	"Squid",
	"Villager",
	"VillagerGolem",
	"Witch",
	"WitherBoss",
	"Wolf",
	"Zombie",
	)

Professions = {
	"Farmer (brown)": 0,
	"Librarian (white)": 1,
	"Priest (purple)": 2,
	"Blacksmith (black apron)": 3,
	"Butcher (white apron)": 4,
	"Villager (green)": 5,
	}
	
ProfessionKeys = ("N/A",)
for key in Professions.keys():
	ProfessionKeys = ProfessionKeys + (key,)

WoolColors={
	"White": 0,
	"Orange": 1,
	"Magenta": 2,
	"Light Blue": 3,
	"Yellow": 4,
	"Lime": 5,
	"Pink": 6,
	"Gray": 7,
	"Light Gray": 8,
	"Cyan": 9,
	"Purple": 10,
	"Blue": 11,
	"Brown": 12,
	"Green": 13,
	"Red": 14,
	"Black": 15,
	"Random": 16
	}

Wools=("White","Orange","Magenta","Light Blue","Yellow","Lime","Pink","Gray","Light Gray","Cyan","Purple","Blue","Brown","Green","Red","Black","Random")
	
Effects = {
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

EffectKeys = ("None",)
for key in Effects.keys():
	EffectKeys = EffectKeys + (key,)
	
noop = -1337
fnoop = -1337.0
inputs = (
	("Operation:",("Fill","Random Fill Number","Random Fill Percent","Grid Fill","Add and Replace Properties","Add Only Potion Effects","Clear All Properties","Output Properties to Console","Set Only Velocity","Set Only Positioning Info","Set Only Spawn Rate Info")),
	("Number or Percentage/Grid Size",10.0),
	("Mob Type",monsters),
	("Block Replace Mode", ("None","Replace","Do Not Replace")),
	("Block to Replace", alphaMaterials.Air),
	("Ticks Until Spawn", noop),
	("Min Ticks Between Spawns (-1337 for Max-1)",noop),
	("Max Ticks Between Spawns",noop),
	("Max Number of Mobs Per Spawn", 4),
	("Potion Effect", EffectKeys),
	("Level",1),
	("Duration (Seconds)", 60),
	("Positioning Mode",("Ignore Values","Relative","Absolute")),
	("PosX",fnoop),
	("PosY",fnoop),
	("PosZ",fnoop),
	("VelocityX", fnoop),
	("VelocityY", fnoop),
	("VelocityZ", fnoop),
	("Can Pick Up Loot",False),
	("Health", noop),
	("Fire", noop),
	("FallDistance", noop),
	("Air", noop),
	("AttackTime", noop),
	("HurtTime", noop),
	("Enderman is Carrying...", alphaMaterials.Air),
	("Villager Profession", ProfessionKeys),
	("Slime Size", noop),
	("Breeding Mode Ticks", noop),
	("Child/Adult Age", noop),
	("Zombie Pig Aggro Level",noop),
	("Whither Skeleton", False),
	("Zombie Villager",False),
	("Powered Creeper", False),
	("Sheep Wool Color", Wools)
)


def perform(level, box, options):
	doreplace = options["Block Replace Mode"]
	blockreplace = options["Block to Replace"]
	delay = options["Ticks Until Spawn"]
	spawndelay = options["Max Ticks Between Spawns"]
	minspawn = options["Min Ticks Between Spawns (-1337 for Max-1)"]
	numspawn = options["Max Number of Mobs Per Spawn"]
	potion = options["Potion Effect"]
	potionlevel = options["Level"]
	potionduration = options["Duration (Seconds)"]
	posmode = options["Positioning Mode"]
	posx = options["PosX"]
	posy = options["PosY"]
	posz = options["PosZ"]
	vx = options["VelocityX"]
	vy = options["VelocityY"]
	vz = options["VelocityZ"]
	looting = options["Can Pick Up Loot"]
	health = options["Health"]
	fire = options["Fire"]
	fall = options["FallDistance"]
	air = options["Air"]
	attack = options["AttackTime"]
	hurt = options["HurtTime"]
	endersteal = options["Enderman is Carrying..."]
	profession = options["Villager Profession"]
	slimesize = options["Slime Size"]
	love = options["Breeding Mode Ticks"]
	age = options["Child/Adult Age"]
	aggro = options["Zombie Pig Aggro Level"]
	whither = options["Whither Skeleton"]
	zomvillager = options["Zombie Villager"]
	powered = options["Powered Creeper"]
	sheepcolor = options["Sheep Wool Color"]

	filltype = options["Operation:"]
	percentage = options["Number or Percentage/Grid Size"]
	mob = options["Mob Type"]

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

	if minspawn != noop:
		if minspawn > 32767:
			minspawn = 32767
		elif minspawn < 0:
			minspawn = 0
	if spawndelay != noop:
		if spawndelay > 32767:
			spawndelay = 32767
		elif spawndelay < 1:
			spawndelay = 1
		if minspawn >= spawndelay:
			minspawn = spawndelay - 1
		spawner_save["MinSpawnDelay"] = TAG_Short(minspawn if minspawn != noop else spawndelay-1)
		spawner_save["MaxSpawnDelay"] = TAG_Short(spawndelay)
	else:
		spawner_save["MinSpawnDelay"] = TAG_Short(200)
		spawner_save["MaxSpawnDelay"] = TAG_Short(800)
		
	if numspawn > 32767:
		numspawn = 32767
	elif numspawn < 0:
		numspawn = 1
	spawner_save["SpawnCount"] = TAG_Short(numspawn)
	
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
	if health != noop:
		entity["Health"] = TAG_Short(health)
	if fire != noop:
		if fire > 32767:
			fire = 32767
		elif fire < -32768:
			fire = -32768
		entity["Fire"] = TAG_Short(fire)
	if fall != noop:
		entity["FallDistance"] = TAG_Float(fall)
	if air != noop:
		if air > 32767:
			air = 32767
		elif air < -32768:
			air = -32768
		entity["Air"] = TAG_Short(air)
	if attack != noop:
		if attack > 32767:
			attack = 32767
		elif attack < -32768:
			attack = -32768
		entity["AttackTime"] = TAG_Short(attack)
	if hurt != noop:
		if hurt > 32767:
			hurt = 32767
		elif hurt < -32768:
			hurt = -32768
		entity["HurtTime"] = TAG_Short(hurt)
		
	entity["CanPickUpLoot"] = TAG_Byte(looting)
	
	if powered and entity["id"].value == "Creeper":
		entity["powered"] = TAG_Byte(1)
	if whither and entity["id"].value == "Skeleton":
		entity["SkeletonType"] = TAG_Byte(1)
	if zomvillager and entity["id"].value == "Zombie":
		entity["IsVillager"] = TAG_Byte(1)
	if endersteal.ID != 0 and entity["id"].value == "Enderman":
		entity["carried"] = TAG_Short(endersteal.ID)
		entity["carriedData"] = TAG_Short(endersteal.blockData)
	if profession != "N/A" and entity["id"].value == "Villager":
		entity["Profession"] = TAG_Int(Professions[profession])
	if slimesize != noop and (entity["id"].value == "Slime" or entity["id"].value == "LavaSlime"):
		entity["Size"] = TAG_Int(slimesize)
	if love != noop:
		entity["InLove"] = TAG_Int(love)
	if age != noop:
		entity["Age"] = TAG_Int(age)
	if aggro != noop and entity["id"].value == "PigZombie":
		if aggro > 32767:
			aggro = 32767
		elif aggro < -32768:
			aggro = -32768
		entity["Anger"] = TAG_Short(aggro);
	if entity["id"].value == "Sheep":
		sheepcolor = WoolColors[sheepcolor]
		if sheepcolor > 0 and sheepcolor < 16:
			entity["Color"] = TAG_Byte(sheepcolor)
	if potion != "None":
		if potionlevel > 127:
			potionlevel = 127
		elif potionlevel < -128:
			potionlevel = -128
		entity["ActiveEffects"] = TAG_List()
		ef = TAG_Compound()
		ef["Amplifier"] = TAG_Byte(potionlevel)
		ef["Id"] = TAG_Byte(Effects[potion])
		ef["Duration"] = TAG_Int(potionduration)
		entity["ActiveEffects"].append(ef)
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
		if entity["EntityId"].value == "Sheep" and sheepcolor == 16:
			entity["Color"] = TAG_Byte(randrange(0,15,1))
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
								if savedentity["EntityId"].value == "Sheep" and WoolColors[sheepcolor] == 16:
									savedentity["Color"] = TAG_Byte(randrange(0,15,1))
								entity["SpawnData"] = savedentity
							else:
								for e in entity_save.keys():
									if e == "ActiveEffects":
										continue
									elif e == "Pos":
										if posmode == "Relative":
											Entity.setpos(entity["SpawnData"],(x+posx,y+posy,z+posz))
										elif posmode == "Absolute":
											entity["SpawnData"]["Pos"] = entity_save["Pos"]
									elif entity["EntityId"].value == "Sheep" and sheepcolor == 16:
										entity["SpawnData"]["Color"] = TAG_Byte(randrange(0,15,1))
									else:
										entity["SpawnData"][e] = entity_save[e]
						if "ActiveEffects" in entity_save:
							if "ActiveEffects" not in entity["SpawnData"]:
								entity["SpawnData"]["ActiveEffects"] = TAG_List()
								entity["SpawnData"]["ActiveEffects"].append(entity_save["ActiveEffects"][0])
							else:
								for ef,trash in enumerate(entity["SpawnData"]["ActiveEffects"]):
									if entity["SpawnData"]["ActiveEffects"][ef]["Id"].value == entity_save["ActiveEffects"][0]["Id"].value:
										entity["SpawnData"]["ActiveEffects"][ef]["Amplifier"] = entity_save["ActiveEffects"][0]["Amplifier"]
										entity["SpawnData"]["ActiveEffects"][ef]["Duration"] = entity_save["ActiveEffects"][0]["Duration"]
										break
								else:
									entity["SpawnData"]["ActiveEffects"].append(entity_save["ActiveEffects"][0])
					elif filltype == "Add Only Potion Effects":
						if "SpawnData" not in entity:
							entity["SpawnData"] = TAG_Compound()
							savedentity = deepcopy(entity_save)
							savedentity["EntityId"] = entity["EntityId"]
							if posmode == "Relative":
								Entity.setpos(savedentity,(x+posx,y+posy,z+posz))
							if savedentity["EntityId"].value == "Sheep" and WoolColors[sheepcolor] == 16:
								savedentity["Color"] = TAG_Byte(randrange(0,15,1))
							entity["SpawnData"] = savedentity
						if "ActiveEffects" in entity_save:
							if "ActiveEffects" not in entity["SpawnData"]:
								entity["SpawnData"]["ActiveEffects"] = TAG_List()
								entity["SpawnData"]["ActiveEffects"].append(entity_save["ActiveEffects"][0])
							else:
								for ef,trash in enumerate(entity["SpawnData"]["ActiveEffects"]):
									if entity["SpawnData"]["ActiveEffects"][ef]["Id"].value == entity_save["ActiveEffects"][0]["Id"].value:
										entity["SpawnData"]["ActiveEffects"][ef]["Amplifier"] = entity_save["ActiveEffects"][0]["Amplifier"]
										entity["SpawnData"]["ActiveEffects"][ef]["Duration"] = entity_save["ActiveEffects"][0]["Duration"]
										break
								else:
									entity["SpawnData"]["ActiveEffects"].append(entity_save["ActiveEffects"][0])
					elif filltype == "Output Properties to Console":
						print entity
					elif filltype == "Set Only Velocity":
						if "SpawnData" not in entity:
							entity["SpawnData"] = TAG_Compound()
							entity["SpawnData"]["EntityId"] = entity["EntityId"]
						entity["SpawnData"]["Motion"] = entity_save["Motion"]
					elif filltype == "Set Only Positioning Info":
						if "SpawnData" not in entity:
							entity["SpawnData"] = TAG_Compound()
							entity["SpawnData"]["EntityId"] = entity["EntityId"]
						if posmode == "Relative":
							Entity.setpos(entity["SpawnData"],(x+posx,y+posy,z+posz))
						else:
							Entity.setpos(entity["SpawnData"],(posx,posy,posz))						
					elif filltype == "Set Only Spawn Rate Info":
						if spawndelay != noop:
							entity["MinSpawnDelay"] = spawner_save["MinSpawnDelay"]
							entity["MaxSpawnDelay"] = spawner_save["MaxSpawnDelay"]
						entity["SpawnCount"] = spawner_save["SpawnCount"]
						if delay != noop:
							entity["Delay"] = spawner_save["Delay"]
						
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

			
