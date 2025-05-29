from pymclevel import TAG_Short
from random import randrange

displayName = "Set Detection Range"

	
inputs = (
	("Set:", ("All","Delay Only","MinSpawnDelay Only","MaxSpawnDelay Only","Detection Radius Only","Max Entities Only", "Spawn Range Only")),
	("Delay Minimum",(20,0,32767)),
	("Delay Maximum",(20,0,32767)),
	("MinSpawnDelay Minimum",(200,0,32767)),
	("MinSpawnDelay Maximum",(200,0,32767)),
	("MaxSpawnDelay Minimum",(800,1,32767)),
	("MaxSpawnDelay Maximum",(800,1,32767)),
	("Player Detection Radius", (15,0,32767)),
	("Maximum Spawned Entities in Area",(4,0,32767)),
	("Spawning Range",(4,0,32767)),
	)

def perform(level, box, options):

	op = options["Set:"]
	delaymin = options["Delay Minimum"]
	delaymax = options["Delay Maximum"]
	mindelaymin = options["MinSpawnDelay Minimum"]
	mindelaymax = options["MinSpawnDelay Maximum"]
	maxdelaymin = options["MaxSpawnDelay Minimum"]
	maxdelaymax = options["MaxSpawnDelay Maximum"]
	playerrange = options["Player Detection Radius"]
	maxentities = options["Maximum Spawned Entities in Area"]
	spawnrange = options["Spawning Range"]

	if delaymin == delaymax:
		delayrand = False
	else:
		delayrand = True
		maxtemp = max(delaymin, delaymax)
		delaymin = min(delaymin, delaymax)
		delaymax = maxtemp

	if mindelaymin == mindelaymax:
		mindelayrand = False
	else:
		mindelayrand = True
		maxtemp = max(mindelaymin, mindelaymax)
		mindelaymin = min(mindelaymin, mindelaymax)
		mindelaymax = maxtemp

	if maxdelaymin == maxdelaymax:
		maxdelayrand = False
	else:
		maxdelayrand = True
		maxtemp = max(maxdelaymin, maxdelaymax)
		maxdelaymin = min(maxdelaymin, maxdelaymax)
		maxdelaymax = maxtemp

	if not maxdelayrand and not mindelayrand:
		if mindelaymin > maxdelaymin:
			temp = mindelaymin
			mindelaymin = maxdelaymin
			maxdelaymin = temp

	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:
				if e["id"].value == "MobSpawner":
					if op == "Delay Only" or op == "All":
						if not delayrand:
							e["Delay"] = TAG_Short(delaymin)
						else:
							e["Delay"] = TAG_Short(randrange(delaymin,delaymax))
					if op == "MinSpawnDelay Only" or op == "All":
						if not mindelayrand:
							e["MinSpawnDelay"] = TAG_Short(mindelaymin)
						else:
							e["MinSpawnDelay"] = TAG_Short(randrange(mindelaymin,mindelaymax))
					if op == "MaxSpawnDelay Only" or op == "All":
						if not maxdelayrand:
							e["MaxSpawnDelay"] = TAG_Short(maxdelaymin)
						else:
							e["MaxSpawnDelay"] = TAG_Short(randrange(maxdelaymin,maxdelaymax))
					if op == "Detection Radius Only" or op == "All":
						e["RequiredPlayerRange"] = TAG_Short(playerrange)
					if op == "Max Entities Only" or op == "All":
						e["MaxNearbyEntities"] = TAG_Short(maxentities)
					if op == "Spawn Range Only" or op == "All":
						e["SpawnRange"] = TAG_Short(spawnrange)

					if e["MinSpawnDelay"].value > e["MaxSpawnDelay"].value:
						temp = e["MaxSpawnDelay"].value
						e["MaxSpawnDelay"] = TAG_Short(e["MinSpawnDelay"].value)
						e["MinSpawnDelay"] = TAG_Short(temp)
					chunk.dirty = True
