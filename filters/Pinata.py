from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float, TAG_Long, TAG_Byte_Array, TAG_Int_Array

displayName = "Chest to Pinata Command Blocks"

fireworktypes = {"Small Ball":0, "Large Ball":1, "Star-shaped":2, "Creeper-shaped":3, "Burst":4}

inputs = [
	(("X Coordinate:",0),
	("Y Coordinate:",3),
	("Z Coordinate:",0),
	("Coordinates are:",("Relative","Absolute")),
	("Prevent TileEntities above and below chests from being overwritten:",True),
	("Use firework explosion effects:", True),
	("All Explosion Effects can take multiple initial and fade colors in a comma-separated list. E.g.: \"#RRGGBB,#RRGGBB\"","label"),
	("Explosion Effect 1:", tuple(["None"],)+tuple(fireworktypes.keys())),
	("Effect 1 Flicker:",False),
	("Effect 1 Trail:",False),
	("Effect 1 Colors:",("string","value=#FFFFFF,#FF0000","width=500")),
	("Effect 1 Fade Colors:",("string","value=#111111,#110000","width=500")),
	("Settings","title")),

	(("Explosion Effect 2:", tuple(["None"],)+tuple(fireworktypes.keys())),
	("Effect 2 Flicker:",False),
	("Effect 2 Trail:",False),
	("Effect 2 Colors:",("string","value=#FFFFFF","width=500")),
	("Effect 2 Fade Colors:",("string","value=#111111","width=500")),
	("Explosion Effect 3:", tuple(["None"],)+tuple(fireworktypes.keys())),
	("Effect 3 Flicker:",False),
	("Effect 3 Trail:",False),
	("Effect 3 Colors:",("string","value=#FFFFFF","width=500")),
	("Effect 3 Fade Colors:",("string","value=#111111","width=500")),
	("Additional Firework Explosions","title"),),
	
	]

def NBT2Command(nbtData):
	command = ""
	if type(nbtData) is TAG_List:
		list = True
	else:
		list = False

	for tag in range(0,len(nbtData)) if list else nbtData.keys():
		if type(nbtData[tag]) is TAG_Compound:
			if not list:
				if tag != "":
					command += tag+":"
			command += "{"
			command += NBT2Command(nbtData[tag])
			command += "}"
		elif type(nbtData[tag]) is TAG_List:
			if not list:
				if tag != "":
					command += tag+":"
			command += "["
			command += NBT2Command(nbtData[tag])
			command += "]"
		else:
			if not list:
				if tag != "":
					command += tag+":"
			if type(nbtData[tag]) is TAG_String:
				command += "\""
				command += str.replace(nbtData[tag].value.encode("unicode-escape"), r'"',r'\\"')
				command += "\""
			else:
				if type(nbtData[tag]) == TAG_Byte_Array:
					command += "["+",".join(["%sb" % num for num in nbtData[tag].value.astype("str")])+"]"
				elif type(nbtData[tag]) == TAG_Int_Array:
					command += "["+",".join(nbtData[tag].value.astype("str"))+"]"
				else:
					command += nbtData[tag].value.encode("unicode-escape") if isinstance(nbtData[tag].value, unicode) else str(nbtData[tag].value)
					if type(nbtData[tag]) is TAG_Byte:
						command += "b"
					elif type(nbtData[tag]) is TAG_Short:
						command += "s"
					elif type(nbtData[tag]) is TAG_Long:
						command += "l"
					elif type(nbtData[tag]) is TAG_Float:
						command += "f"
					elif type(nbtData[tag]) is TAG_Double:
						command += "d"			
		command += ","
	else:
		if command != "":
			if command[-1] == ",":
				command = command[:-1]
	return command

def CommandBlock(x,y,z,command):
	cmd = TAG_Compound()
	cmd["x"] = TAG_Int(x)
	cmd["y"] = TAG_Int(y)
	cmd["z"] = TAG_Int(z)
	cmd["id"] = TAG_String("Control")
	cmd["Command"] = TAG_String(command)
	cmd["TrackOutput"] = TAG_Byte(0)
	return cmd


def perform(level, box, options):
	dx = options["X Coordinate:"]
	dy = options["Y Coordinate:"]
	dz = options["Z Coordinate:"]
	relative = True if options["Coordinates are:"] == "Relative" else False
	
	nooverwrite = options["Prevent TileEntities above and below chests from being overwritten:"]
	fireworks = options["Use firework explosion effects:"]
	
	if fireworks and (options["Explosion Effect 1:"] != "None" or options["Explosion Effect 2:"] != "None" or options["Explosion Effect 3:"] != "None"):
		fw = TAG_Compound()
		fw["LifeTime"] = TAG_Int(-1)
		fw["Life"] = TAG_Int(2)
		fw["FireworksItem"] = TAG_Compound()
		fw["FireworksItem"]["id"] = TAG_Short(401)
		fw["FireworksItem"]["tag"] = TAG_Compound()
		fw["FireworksItem"]["tag"]["Fireworks"] = TAG_Compound()
		fw["FireworksItem"]["tag"]["Fireworks"]["Explosions"] = TAG_List()
		
		for i in xrange(1,4):
			if options["Explosion Effect "+str(i)+":"] != "None":
				exp = TAG_Compound()
				exp["Type"] = TAG_Byte(fireworktypes[options["Explosion Effect "+str(i)+":"]])
				if options["Effect "+str(i)+" Flicker:"]:
					exp["Flicker"] = TAG_Byte(options["Effect "+str(i)+" Flicker:"])
				if options["Effect "+str(i)+" Trail:"]:
					exp["Trail"] = TAG_Byte(options["Effect "+str(i)+" Trail:"])
				colors = []
				for color in options["Effect "+str(i)+" Colors:"].split(","):
					if color[0] != "#":
						continue
					if len(color) > 7:
						colors.append(int(color[1:],16))
					else:
						colors.append(int(color[1:7],16))
				if colors:
					exp["Colors"] = TAG_List()
					for c in colors:
						exp["Colors"].append(TAG_Int(c))
				else:
					raise ValueError("ERROR! There are no valid color values provided for explosion effect #"+str(i)+"!")
				fadecolors = []
				for color in options["Effect "+str(i)+" Fade Colors:"].split(","):
					if color[0] != "#":
						continue
					if len(color) > 7:
						fadecolors.append(int(color[1:],16))
					else:
						fadecolors.append(int(color[1:7],16))
				if fadecolors:
					exp["FadeColors"] = TAG_List()
					for c in fadecolors:
						exp["FadeColors"].append(TAG_Int(c))
				fw["FireworksItem"]["tag"]["Fireworks"]["Explosions"].append(exp)

		fwstring = "{"+NBT2Command(fw)+"}"
	else:
		fireworks = False

	entsToAdd = []
	entsToDelete = []
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:
				if e["id"].value == "Chest":
					if "Items" not in e:
						continue
					if len(e["Items"]) == 0:
						continue

					ent = level.tileEntityAt(x,y+1,z)
					if ent != None:
						if nooverwrite:
							print "Detected TileEntity above Chest at",x,y,z," Skipping."
							continue
						else:
							entsToDelete.append((chunk,ent))
					if fireworks:
						ent = level.tileEntityAt(x,y-1,z)
						if ent != None:
							if nooverwrite:
								print "Detected TileEntity below Chest at",x,y,z," Skipping."
								continue
							else:
								entsToDelete.append((chunk,ent))

					entsToDelete.append((chunk,e))

					level.setBlockAt(x, y+1, z, 137)
					level.setBlockDataAt(x, y+1, z, 0)
					if relative:
						com = "setblock ~"+str(dx)+" ~"+str(dy-1)+" ~"+str(dz)+" air"
						entsToAdd.append((chunk,CommandBlock(x,y+1,z,com)))
					else:
						com = "setblock "+str(dx)+" "+str(dy)+" "+str(dz)+" air"
						entsToAdd.append((chunk,CommandBlock(x,y+1,z,com)))
					
					level.setBlockAt(x, y, z, 137)
					level.setBlockDataAt(x, y, z, 0)
					if relative:
						entsToAdd.append((chunk,CommandBlock(x,y,z,unicode("setblock ~{} ~{} ~{} chest 0 replace {}".format(unicode(dx), unicode(dy), unicode(dz), unicode("{Items:["+NBT2Command(e["Items"])+"]}")).decode("unicode-escape")))))
					else:
						entsToAdd.append((chunk,CommandBlock(x,y,z,unicode("setblock {} {} {} chest 0 replace {}".format(unicode(dx), unicode(dy), unicode(dz), unicode("{Items:["+NBT2Command(e["Items"])+"]}")).decode("unicode-escape")))))
					
					if fireworks:
						level.setBlockAt(x, y-1, z, 137)
						level.setBlockDataAt(x, y-1, z, 0)
						if relative:
							com = "summon FireworksRocketEntity ~"+str(dx)+" ~"+str(dy+1)+" ~"+str(dz) +" "+ fwstring
							entsToAdd.append((chunk,CommandBlock(x,y-1,z,com)))
						else:
							com = "summon FireworksRocketEntity "+str(dx)+" "+str(dy)+" "+str(dz) +" "+ fwstring
							entsToAdd.append((chunk,CommandBlock(x,y-1,z,com)))
					

	for (chunk, entity) in entsToAdd:
		chunk.TileEntities.append(entity)
		chunk.dirty = True
				
	for (chunk, entity) in entsToDelete:
		chunk.TileEntities.remove(entity)
		chunk.dirty = True


