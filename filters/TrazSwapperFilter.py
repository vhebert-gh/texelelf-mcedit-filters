from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float
from pymclevel.materials import alphaMaterials
import math
import inspect
from pymclevel import MCSchematic
from copy import deepcopy


displayName = "TrazLander's Swapper Filter"

inputs = [
	(("Operation:",("Swap Blocks","Drop Blocks","Spawn Blocks","Recalculate Minecart Positions")),
	("Spawn Type:",("Command Block","Generation 2","Generation 1")),
	("Swap Selected Blocks With:", alphaMaterials.Stone),
	("Spawner Player Detection Radius (Gen 1 Only):",(512,-32768,32767)),
	("Maximum Number of Layers in Schematic (Gen 1 Only):",(8,1,50)),
	("ALWAYS run a \"Recalculate Minecart Positions\" operation after importing Generation 1 and 2 Swapper schematics or moving Generation 1 & 2 Swapper spawners!!","label"),
	("General","title"),),
	
	(("Block Filtering:", ("None","Only the Below","Except the Below")),
	("Ignore Damage Value",False),
	("Filter Block 1", alphaMaterials.Air),
	("Filter Block 2", alphaMaterials.Air),
	("Filter Block 3", alphaMaterials.Air),
	("Filter Block 4", alphaMaterials.Air),
	("Filter Block 5", alphaMaterials.Air),
	("Filter Block 6", alphaMaterials.Air),
	("Filter Block 7", alphaMaterials.Air),
	("Filter Block 8", alphaMaterials.Air),
	("Block Filtering","title"),),
	]

def DrawActivator(level, bx, by, bz):
	Activator = [[[(0,0),(0,0),(0,0)],[(0,0),(52,0),(0,0)],[(0,0),(0,0),(0,0)],[(0,0),(52,0),(0,0)],[(0,0),(0,0),(0,0)]],
				[[(1,0),(20,0),(0,0)],[(23,5),(0,0),(89,0)],[(1,0),(89,0),(1,0)],[(23,5),(0,0),(89,0)],[(1,0),(20,0),(0,0)]],
				[[(55,0),(0,0),(0,0)],[(93,8),(0,0),(0,0)],[(55,0),(55,0),(93,1)],[(93,10),(0,0),(0,0)],[(55,0),(0,0),(0,0)]]]
	startx = x = bx
	starty = y = by
	startz = z = bz
	for ix in xrange(3):
		z = startz
		for iy in xrange(5):
			x = startx
			for id, data in Activator[ix][iy]:
				if id != 0:
					level.setBlockAt(x, y, z, id)
					level.setBlockDataAt(x, y, z, data)
				x += 1
			z += 1
		y += 1
	return

def DeletePad(level,bx,by,bz):
	for x in xrange(0,2):
		for z in xrange(3,5):
			for y in xrange(3):
				level.setBlockAt(bx+x, by+y, bz+z, 0)
				level.setBlockDataAt(bx+x, by+y, bz+z, 0)
				

def DrawGen2Activator(level, bx, by, bz):
	Activator = [[(0,0),(55,15),(55,14),(55,13),(0,0),(55,0),(55,0),(55,0),(0,0),(0,0)],
				[(0,0),(76,4),(89,0),(55,12),(0,0),(55,0),(89,0),(93,2),(89,0),(0,0)],
				[(93,1),(1,0),(93,9),(1,0),(75,1),(55,0),(93,13),(23,5),(0,0),(20,0)],
				[(89,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(89,0),(0,0)],]
	dispenser = TAG_Compound()
	dispenser["id"] = TAG_String("Trap")
	dispenser["Items"] = TAG_List()
	dispenser["Items"].append(TAG_Compound())
	dispenser["Items"][0]["Slot"] = TAG_Byte(4)
	dispenser["Items"][0]["id"] = TAG_Short(327)
	dispenser["Items"][0]["Damage"] = TAG_Short(0)
	dispenser["Items"][0]["Count"] = TAG_Byte(1)
	dispenser["x"] = TAG_Int(bx+7)
	dispenser["y"] = TAG_Int(by)
	dispenser["z"] = TAG_Int(bz+2)
	level.TileEntities.append(dispenser)
	startx = x = bx
	y = by
	startz = z = bz
	for ix in xrange(4):
		x = startx
		for id, data in Activator[ix]:
			if id != 0:
				if id == 93 or id == 55:
					level.setBlockAt(x, y-1, z, 1)
					level.setBlockDataAt(x, y-1, z, 0)
				level.setBlockAt(x, y, z, id)
				level.setBlockDataAt(x, y, z, data)
			x += 1
		z += 1
	level.setBlockAt(bx+8, y-1, bz+2, 1)
	level.setBlockDataAt(x+8, y-1, bz+2, 0)
	return
	
def DrawActivationLine(level,x,y,z,length):
	for px in xrange(x, x-length, -1):
		if abs(px-x)%16:
			level.setBlockAt(px, y, z, 55)
			level.setBlockDataAt(px, y, z, 0)			
			level.setBlockAt(px, y-1, z, 1)
			level.setBlockDataAt(px, y-1, z, 0)	
		elif abs(px-x) != 0:
			level.setBlockAt(px, y, z, 93)
			level.setBlockDataAt(px, y, z, 1)
			level.setBlockAt(px, y, z+1, 89)
			level.setBlockDataAt(px, y, z+1, 0)
			level.setBlockAt(px, y-1, z, 1)
			level.setBlockDataAt(px, y-1, z, 0)	

def perform(level, box, options):
	editor = inspect.stack()[1][0].f_locals.get('self', None).editor

	op = options["Operation:"]
	swap = options["Swap Selected Blocks With:"]
	range = options["Spawner Player Detection Radius (Gen 1 Only):"]
	maxrows = options["Maximum Number of Layers in Schematic (Gen 1 Only):"]
	type = options["Spawn Type:"]
	
	filter = options["Block Filtering:"]
	ignore = options["Ignore Damage Value"]

	FilterBlock = []
	
	if options["Filter Block 1"].ID != 0:
		FilterBlock.append((options["Filter Block 1"].ID,(options["Filter Block 1"].blockData if not ignore else 0)))
	if options["Filter Block 2"].ID != 0:
		FilterBlock.append((options["Filter Block 2"].ID,(options["Filter Block 2"].blockData if not ignore else 0)))
	if options["Filter Block 3"].ID != 0:
		FilterBlock.append((options["Filter Block 3"].ID,(options["Filter Block 3"].blockData if not ignore else 0)))
	if options["Filter Block 4"].ID != 0:
		FilterBlock.append((options["Filter Block 4"].ID,(options["Filter Block 4"].blockData if not ignore else 0)))
	if options["Filter Block 5"].ID != 0:
		FilterBlock.append((options["Filter Block 5"].ID,(options["Filter Block 5"].blockData if not ignore else 0)))
	if options["Filter Block 6"].ID != 0:
		FilterBlock.append((options["Filter Block 6"].ID,(options["Filter Block 6"].blockData if not ignore else 0)))
	if options["Filter Block 7"].ID != 0:
		FilterBlock.append((options["Filter Block 7"].ID,(options["Filter Block 7"].blockData if not ignore else 0)))
	if options["Filter Block 8"].ID != 0:
		FilterBlock.append((options["Filter Block 8"].ID,(options["Filter Block 8"].blockData if not ignore else 0)))	
	if op == "Recalculate Minecart Positions":
		if type == "Generation 1":
			for (chunk, slices, point) in level.getChunkSlices(box):
				for e in chunk.TileEntities:
					x = e["x"].value
					y = e["y"].value
					z = e["z"].value
					if (x,y,z) in box:
						if e["id"].value != "MobSpawner":
							continue
						if "EntityId" not in e:
							continue
						if e["EntityId"].value != "MinecartSpawner":
							continue
						if "SpawnData" in e:
							if "Pos" in e["SpawnData"]:
								e["SpawnData"]["Pos"][0] = TAG_Double(x+0.5)
								e["SpawnData"]["Pos"][1] = TAG_Double(y+1.5)
								e["SpawnData"]["Pos"][2] = TAG_Double(z+0.5)
						if "SpawnPotentials" in e:
							if len(e["SpawnPotentials"]) > 0:
								if "Properties" in e["SpawnPotentials"][0]:
									if "Pos" in e["SpawnPotentials"][0]["Properties"]:
										e["SpawnPotentials"][0]["Properties"]["Pos"][0] = TAG_Double(x+0.5)
										e["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(y+1.5)
										e["SpawnPotentials"][0]["Properties"]["Pos"][2] = TAG_Double(z+0.5)
						chunk.dirty = True
		elif type == "Generation 2":
			ex = ey = ez = None
			numspawners = 0
			for (chunk, slices, point) in level.getChunkSlices(box):
				for e in chunk.TileEntities:
					x = e["x"].value
					y = e["y"].value
					z = e["z"].value
					if (x,y,z) in box:
						if e["id"].value != "MobSpawner":
							continue
						if "EntityId" not in e:
							continue
						if e["EntityId"].value != "MinecartSpawner":
							continue
						numspawners += 1
			for (chunk, slices, point) in level.getChunkSlices(box):
				for e in chunk.TileEntities:
					x = e["x"].value
					y = e["y"].value
					z = e["z"].value
					if (x,y,z) in box:
						if e["id"].value != "Trap":
							continue
						ex = x + 1
						ey = y
						ez = z
						break
				if ex != None:
					break
			else:
				print "ERROR: Unable to find Dispenser for recalculation!"
			for (chunk, slices, point) in level.getChunkSlices(box):
				for e in chunk.TileEntities:
					x = e["x"].value
					y = e["y"].value
					z = e["z"].value
					if (x,y,z) in box:
						if e["id"].value != "MobSpawner":
							continue
						if "EntityId" not in e:
							continue
						if e["EntityId"].value != "MinecartSpawner":
							continue
						e["MaxNearbyEntities"] = TAG_Short(numspawners)
						if ex > x:
							newx = ex - x
						else:
							newx = x - ex
						if ez > z:
							newz = ez - z
						else:
							newz = z - ez
						e["SpawnRange"] = TAG_Short(int(max(newx,newz)))
						if "SpawnData" in e:
							if "Pos" in e["SpawnData"]:
								e["SpawnData"]["Pos"][0] = TAG_Double(ex+0.5)
								e["SpawnData"]["Pos"][1] = TAG_Double(ey+0.5)
								e["SpawnData"]["Pos"][2] = TAG_Double(ez+0.5)
						if "SpawnPotentials" in e:
							if len(e["SpawnPotentials"]) > 0:
								if "Properties" in e["SpawnPotentials"][0]:
									if "Pos" in e["SpawnPotentials"][0]["Properties"]:
										e["SpawnPotentials"][0]["Properties"]["Pos"][0] = TAG_Double(ex+0.5)
										e["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(ey+0.5)
										e["SpawnPotentials"][0]["Properties"]["Pos"][2] = TAG_Double(ez+0.5)
						chunk.dirty = True
		return
	
	if (op == "Spawn Blocks" or op == "Swap Blocks") and swap.ID == 0:
		print "Error!  Minecraft cannot spawn Air blocks.  To delete blocks, use the \"Drop Blocks\" operation."
		return

	dispenser = TAG_Compound()
	dispenser["id"] = TAG_String("Trap")
	dispenser["Items"] = TAG_List()
	dispenser["Items"].append(TAG_Compound())
	dispenser["Items"][0]["Slot"] = TAG_Byte(4)
	dispenser["Items"][0]["id"] = TAG_Short(327)
	dispenser["Items"][0]["Damage"] = TAG_Short(0)
	dispenser["Items"][0]["Count"] = TAG_Byte(1)

	spawner = TAG_Compound()
	spawner["id"] = TAG_String("MobSpawner")
	spawner["EntityId"] = TAG_String("MinecartSpawner")

	spawner["SpawnCount"] = TAG_Short(1)
	spawner["SpawnRange"] = TAG_Short(0)
	spawner["MaxNearbyEntities"] = TAG_Short(1)
	spawner["RequiredPlayerRange"] = TAG_Short(range)
	spawner["Delay"] = TAG_Short(1)
	spawner["MinSpawnDelay"] = TAG_Short(10)
	spawner["MaxSpawnDelay"] = TAG_Short(10)
	spawner["SpawnPotentials"] = TAG_List()
	spawner["SpawnPotentials"].append(TAG_Compound())
	spawner["SpawnPotentials"][0]["Type"] = TAG_String("MinecartSpawner")
	spawner["SpawnPotentials"][0]["Weight"] = TAG_Int(1)
	
	cart = TAG_Compound()
	cart["id"] = TAG_String("MinecartSpawner")
	cart["EntityId"] = TAG_String("FallingSand")

	cart["SpawnCount"] = TAG_Short(1)
	cart["SpawnRange"] = TAG_Short(0)
	cart["MaxNearbyEntities"] = TAG_Short(1)
	cart["RequiredPlayerRange"] = TAG_Short(range)
	cart["Delay"] = TAG_Short(1)
	cart["MinSpawnDelay"] = TAG_Short(32766)
	cart["MaxSpawnDelay"] = TAG_Short(32767)

	cart["Rotation"] = TAG_List()
	cart["Rotation"].append(TAG_Float(0.0))
	cart["Rotation"].append(TAG_Float(0.0))
	cart["CustomDisplayTile"] = TAG_Byte(1)
	cart["SpawnPotentials"] = TAG_List()
	cart["SpawnPotentials"].append(TAG_Compound())
	cart["SpawnPotentials"][0]["Type"] = TAG_String("FallingSand")
	cart["SpawnPotentials"][0]["Weight"] = TAG_Int(1)
	cart["Pos"] = TAG_List()
	cart["Pos"].append(TAG_Double(0.0))
	cart["Pos"].append(TAG_Double(0.0))
	cart["Pos"].append(TAG_Double(0.0))
	cart["SpawnData"] = TAG_Compound()
	cart["SpawnData"]["id"] = TAG_String("FallingSand")
	cart["SpawnData"]["FallDistance"] = TAG_Float(0.0)
	cart["SpawnData"]["DropItem"] = TAG_Byte(0)
	cart["SpawnData"]["Pos"] = TAG_List()
	cart["SpawnData"]["Pos"].append(TAG_Double(0.0))
	cart["SpawnData"]["Pos"].append(TAG_Double(-1.0))
	cart["SpawnData"]["Pos"].append(TAG_Double(0.0))
	cart["SpawnData"]["TileID"] = TAG_Int(1)
	cart["SpawnData"]["Data"] = TAG_Byte(0)
	cart["SpawnData"]["Time"] = TAG_Byte(100)

	sx,sy,sz = box.size
	if type == "Generation 1":
		width = (sx * 2)+2# if op != "Swap Blocks" else 4)
		height = min(maxrows,sy) * 3
		length = (sz * math.ceil(float(sy)/float(maxrows))) * 6
		schematic = MCSchematic((width, height, length), mats=level.materials)

		zctr = 0
		for z in xrange(box.minz, box.maxz):
			pz = zctr * 6
			yctr = 0
			for y in xrange(box.miny, box.maxy):
				if yctr >= maxrows:
					pz += 6
					zctr += 1
					yctr = 0
				py = yctr * 3
				xoff = yctr % 2
				xctr = 0
				for x in xrange(box.minx, box.maxx):
					block = level.blockAt(x, y, z)
					if block == 0:
						continue
					data = level.blockDataAt(x, y, z)
					if filter != "None":
						if filter == "Only the Below" and ((block,(data if not ignore else 0)) not in FilterBlock):
							continue
						elif filter == "Except the Below" and ((block,(data if not ignore else 0)) in FilterBlock):
							continue
					if op == "Swap Blocks":
						px = (xctr * 2 + (1 * (xctr / 7))) + xoff
						DrawActivator(schematic, px, py, pz)
					else:
						if not xctr % 2:
							px = (xctr + (1 * (xctr / 14))) + xoff
							DrawActivator(schematic, px, py, pz)
						else:
							px = ((xctr-1) + (1 * (xctr / 14))) + xoff
					for lp in xrange(2):
						if op == "Swap Blocks":
							if not lp:
								zoff = 1
							else:
								zoff = 3
						else:
							if not xctr % 2:
								zoff = 1
							else:
								zoff = 3
						disp = deepcopy(dispenser)
						disp["x"] = TAG_Int(px)
						disp["y"] = TAG_Int(py+1)
						disp["z"] = TAG_Int(pz+zoff)
						schematic.TileEntities.append(disp)
						spwn = deepcopy(spawner)
						spwn["x"] = TAG_Int(px+1)
						spwn["y"] = TAG_Int(py)
						spwn["z"] = TAG_Int(pz+zoff)
						crt = deepcopy(cart)
						crt["SpawnData"]["Pos"][0] = TAG_Double(x+0.5)
						if op == "Swap Blocks":
							if block != swap.ID and not lp:
								crt["SpawnData"]["Pos"][1] = TAG_Double(y+0.75)
							else:
								crt["SpawnData"]["Pos"][1] = TAG_Double(y+0.25)
						else:
							crt["SpawnData"]["Pos"][1] = TAG_Double(y+0.5)
						crt["SpawnData"]["Pos"][2] = TAG_Double(z+0.5)
						
						if op == "Swap Blocks":
							if not lp: #old block
								crt["SpawnData"]["Time"] = TAG_Byte(0)
								crt["SpawnData"]["TileID"] = TAG_Int(block)
								if block == swap.ID:
									crt["SpawnData"]["Data"] = TAG_Byte(swap.blockData)
								else:
									crt["SpawnData"]["Data"] = TAG_Byte(data)
								crt["DisplayTile"] = TAG_Int(block)
								crt["DisplayData"] = TAG_Int(data)
							else:
								crt["SpawnData"]["Time"] = TAG_Byte(1)
								crt["SpawnData"]["TileID"] = TAG_Int(swap.ID)
								crt["SpawnData"]["Data"] = TAG_Byte(swap.blockData)
								crt["DisplayTile"] = TAG_Int(swap.ID)
								crt["DisplayData"] = TAG_Int(swap.blockData)

						elif op == "Drop Blocks":
							crt["SpawnData"]["Time"] = TAG_Byte(0)
							crt["SpawnData"]["TileID"] = TAG_Int(block)
							crt["SpawnData"]["Data"] = TAG_Byte(data)
							crt["DisplayTile"] = TAG_Int(block)
							crt["DisplayData"] = TAG_Int(data)
						else:
							crt["SpawnData"]["Time"] = TAG_Byte(2)
							crt["SpawnData"]["TileID"] = TAG_Int(block)
							crt["SpawnData"]["Data"] = TAG_Byte(data)
							crt["DisplayTile"] = TAG_Int(block)
							crt["DisplayData"] = TAG_Int(data)
						crt["SpawnPotentials"][0]["Properties"] = deepcopy(crt["SpawnData"])
						crt["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(-1.0)
						spwn["SpawnData"] = deepcopy(crt)
						spwn["SpawnPotentials"][0]["Properties"] = deepcopy(crt)
						schematic.TileEntities.append(spwn)
						pl = deepcopy(crt)
						pl["SpawnData"]["Pos"][1] = TAG_Double(-1.0)
						pl["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(-1.0)
						pl["RequiredPlayerRange"] = TAG_Short(0)
						pl["OnGround"] = TAG_Byte(1)
						pl["Motion"] = TAG_List()
						pl["Motion"].append(TAG_Double(0.0))
						pl["Motion"].append(TAG_Double(0.0))
						pl["Motion"].append(TAG_Double(0.0))
						pl["Pos"][0] = TAG_Double(px+1.5)
						pl["Pos"][1] = TAG_Double(py+1.5)
						pl["Pos"][2] = TAG_Double(pz+zoff+0.5)
						schematic.Entities.append(pl)
						
						if op == "Swap Blocks":
							if block == swap.ID:
								DeletePad(schematic,px, py, pz)
								break
						else:
							break
					xctr += 1
				else:
					if op != "Swap Blocks" and xctr % 2:
						DeletePad(schematic,px, py, pz)
				yctr += 1
			zctr += 1
	elif type == "Generation 2":
		width = max(10,sx * (1 if op != "Swap Blocks" else 2))
		height = 9
		length = max(4,((sz+1) * (math.ceil(float(sy/8))+1))-1)
		schematic = MCSchematic((width, height, length), mats=level.materials)
		
		px = (width/2) - 5
		pz = (length/2) - 2
		DrawGen2Activator(schematic, px, 4, pz)
		DrawActivationLine(schematic,px,4,pz+2,(width/2)-1)

		spawnpointx = px + 8
		spawnpointz = pz + 2

		for y in xrange(box.miny, box.maxy):
			extrawidth = (y - box.miny) % 8
			if extrawidth >= 4:
				ey = extrawidth + 1
			else:
				ey = extrawidth
			for z in xrange(box.minz, box.maxz):
				ez = (z-box.minz) + ((y - box.miny)/8 * (sz + 1))
				for x in xrange(box.minx, box.maxx):
					block = level.blockAt(x, y, z)
					if block == 0:
						continue
					data = level.blockDataAt(x, y, z)
					ex = (x - box.minx) * (2 if op == "Swap Blocks" else 1)
					if filter != "None":
						if filter == "Only the Below" and ((block,(data if not ignore else 0)) not in FilterBlock):
							continue
						elif filter == "Except the Below" and ((block,(data if not ignore else 0)) in FilterBlock):
							continue
					for lp in xrange(2):
						if lp:
							ex += 1
						schematic.setBlockAt(ex, ey, ez, 52)
						schematic.setBlockDataAt(ex, ey, ez, 0)
						spwn = deepcopy(spawner)
						spwn["x"] = TAG_Int(ex)
						spwn["y"] = TAG_Int(ey)
						spwn["z"] = TAG_Int(ez)
						crt = deepcopy(cart)
						crt["SpawnData"]["Pos"][0] = TAG_Double(x+0.5)
						if op == "Swap Blocks":
							if block != swap.ID and not lp:
								crt["SpawnData"]["Pos"][1] = TAG_Double(y+0.75)
							else:
								crt["SpawnData"]["Pos"][1] = TAG_Double(y+0.25)
						else:
							crt["SpawnData"]["Pos"][1] = TAG_Double(y+0.5)
						crt["SpawnData"]["Pos"][2] = TAG_Double(z+0.5)

						if op == "Swap Blocks":
							if not lp: #old block
								crt["SpawnData"]["Time"] = TAG_Byte(0)
								crt["SpawnData"]["TileID"] = TAG_Int(block)
								if block == swap.ID:
									crt["SpawnData"]["Data"] = TAG_Byte(swap.blockData)
								else:
									crt["SpawnData"]["Data"] = TAG_Byte(data)
								crt["DisplayTile"] = TAG_Int(block)
								crt["DisplayData"] = TAG_Int(data)
							else:
								crt["SpawnData"]["Time"] = TAG_Byte(1)
								crt["SpawnData"]["TileID"] = TAG_Int(swap.ID)
								crt["SpawnData"]["Data"] = TAG_Byte(swap.blockData)
								crt["DisplayTile"] = TAG_Int(swap.ID)
								crt["DisplayData"] = TAG_Int(swap.blockData)

						elif op == "Drop Blocks":
							crt["SpawnData"]["Time"] = TAG_Byte(0)
							crt["SpawnData"]["TileID"] = TAG_Int(block)
							crt["SpawnData"]["Data"] = TAG_Byte(data)
							crt["DisplayTile"] = TAG_Int(block)
							crt["DisplayData"] = TAG_Int(data)
						else:
							crt["SpawnData"]["Time"] = TAG_Byte(2)
							crt["SpawnData"]["TileID"] = TAG_Int(block)
							crt["SpawnData"]["Data"] = TAG_Byte(data)
							crt["DisplayTile"] = TAG_Int(block)
							crt["DisplayData"] = TAG_Int(data)
						crt["SpawnPotentials"][0]["Properties"] = deepcopy(crt["SpawnData"])
						crt["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(-1.0)
						spwn["SpawnData"] = deepcopy(crt)
						spwn["SpawnPotentials"][0]["Properties"] = deepcopy(crt)
						schematic.TileEntities.append(spwn)
						pl = deepcopy(crt)
						pl["SpawnData"]["Pos"][1] = TAG_Double(-1.0)
						pl["SpawnPotentials"][0]["Properties"]["Pos"][1] = TAG_Double(-1.0)
						pl["RequiredPlayerRange"] = TAG_Short(0)
						pl["OnGround"] = TAG_Byte(1)
						pl["Motion"] = TAG_List()
						pl["Motion"].append(TAG_Double(0.0))
						pl["Motion"].append(TAG_Double(0.0))
						pl["Motion"].append(TAG_Double(0.0))
						pl["Pos"][0] = TAG_Double(spawnpointx+0.5)
						pl["Pos"][1] = TAG_Double(4.5)
						pl["Pos"][2] = TAG_Double(spawnpointz+0.5)
						schematic.Entities.append(pl)
						
						if op == "Swap Blocks":
							if block == swap.ID:
								break
						else:
							break
	elif type == "Command Block":
		width = sx + math.ceil(float(sx)/float(15))
		height = sy * 2
		length = sz * (3 + math.ceil(float(sz)/float(15)))
		schematic = MCSchematic((width, height, length), mats=level.materials)

		zadd = 0
		yctr = 0
		for y in xrange(box.miny, box.maxy):
			zctr = 0
			for z in xrange(box.minz, box.maxz):
				xctr = 0
				blockcounter = 0
				xadd = 0
				for x in xrange(box.minx, box.maxx):
					block = level.blockAt(x, y, z)
					if block == 0:
						continue
					data = level.blockDataAt(x, y, z)
					if filter != "None":
						if filter == "Only the Below" and ((block,(data if not ignore else 0)) not in FilterBlock):
							continue
						elif filter == "Except the Below" and ((block,(data if not ignore else 0)) in FilterBlock):
							continue

					for lp in xrange(2):
						xPos = float(x)+0.5
						if op == "Swap Blocks":
							if block != swap.ID and not lp:
								yPos = float(y)+0.75
							else:
								yPos = float(y)+0.25
						else:
							yPos = float(y)+0.5
						zPos = float(z)+0.5
						
						if op == "Swap Blocks":
							if not lp: #old block
								time = 0
								tileid = block
								if block == swap.ID:
									blockdata = swap.blockData
								else:
									blockdata = data
							else:
								time = 1
								tileid = swap.ID
								blockdata = swap.blockData

						elif op == "Drop Blocks":
								time = 0
								tileid = block
								blockdata = data
						else:
							time = 2
							tileid = block
							blockdata = data
						
						if not lp:
							zadd = 0
						else:
							zadd = 2
						command = "summon FallingSand "+str(xPos)+" "+str(yPos)+" "+str(zPos)+" {Time:"+str(time)+",TileID:"+str(tileid)+",Data:"+str(blockdata)+",FallDistance:0.0,DropItem:0}"

						newcommand = TAG_Compound()
						newcommand["id"] = TAG_String("Control")
						newcommand["x"] = TAG_Int(xctr+xadd)
						newcommand["y"] = TAG_Int(yctr*2)
						newcommand["z"] = TAG_Int((zctr*3)+zadd)
						newcommand["SuccessCount"] = TAG_Int(0)
						newcommand["Command"] = TAG_String(command)

						schematic.setBlockAt(xctr+xadd, yctr*2, (zctr*3)+zadd, 137)
						schematic.setBlockDataAt(xctr+xadd, yctr*2, (zctr*3)+zadd, 0)
						schematic.TileEntities.append(newcommand)
						if not lp:
							schematic.setBlockAt(xctr+xadd, yctr*2, (zctr*3)+zadd+1, 1)
							schematic.setBlockDataAt(xctr+xadd, yctr*2, (zctr*3)+zadd+1, 0)
							schematic.setBlockAt(xctr+xadd, (yctr*2)+1, (zctr*3)+zadd+1, 55)
							schematic.setBlockDataAt(xctr+xadd, (yctr*2)+1, (zctr*3)+zadd+1, 0)
						
						blockcounter += 1
						
						if blockcounter == 30:
							blockcounter = 0
							xadd += 1
							schematic.setBlockAt(xctr+xadd, (yctr*2)+1, (zctr*3)+zadd-2, 89)
							schematic.setBlockDataAt(xctr+xadd, (yctr*2)+1, (zctr*3)+zadd-2, 0)
							schematic.setBlockAt(xctr+xadd, yctr*2, (zctr*3)+zadd-1, 1)
							schematic.setBlockDataAt(xctr+xadd, yctr*2, (zctr*3)+zadd-1, 0)
							schematic.setBlockAt(xctr+xadd, (yctr*2)+1, (zctr*3)+zadd-1, 93)
							schematic.setBlockDataAt(xctr+xadd, (yctr*2)+1, (zctr*3)+zadd-1, 1)

						if op == "Swap Blocks":
							if block == swap.ID:
								break
						else:
							break
					xctr += 1
				zctr += 1
			yctr += 1

	editor.addCopiedSchematic(schematic)
	raise Exception("Schematic successfully added to clipboard.")
