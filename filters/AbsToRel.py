from pymclevel import TAG_String

displayName = "Absolute to Relative Coordinates"

command_types = ["setblock","testforblock ","testforblocks","blockdata","summon","clone","fill","particle","playsound","spreadplayers"]

inputs = (("Operate on:",("Command Blocks","Command Block Minecarts")),
	("Command Type:",tuple(("All",))+tuple(command_types)),
	("Coordinate Conversion:",( "Absolute Coordinates -> Relative Coordinates",
								"Relative Coordinates -> Absolute Coordinates",
								"Offset Coordinates",
								"Remove Decimal Places",
								"Add Decimal Places")),
	("X Offset",0.0),
	("Y Offset",0.0),
	("Z Offset",0.0),
	("Apply to Coordinate Sets (clone and fill only):",("All","First and Second (clone, testforblocks src\\fill dest.)","First","Second","Third (clone, testforblocks dest.)")),
	)

FIRST = 1
SECOND = 2
THIRD = 4

TORELATIVE = 0
TOABSOLUTE = 1
OFFSET = 2
REMOVEDEC = 3
ADDDEC = 4
	
def convertValue(val,offset,op):
	if val == None:
		return None
	if "." in val or "." in str(offset):
		fv = True
	else:
		fv = False

	if val == "~":
		if op == TORELATIVE or op == REMOVEDEC:
			return val
		elif op == TOABSOLUTE:
			return str(offset)
		elif op == OFFSET:
			return val+str(offset)
		elif op == ADDDEC:
			return val+"0.0"
	elif val[0] == "~":
		if op == TORELATIVE:
			return val
		elif op == TOABSOLUTE:
			if fv:
				return str(float(val.lstrip("~")) + offset)
			else:
				return str(int(val.lstrip("~")) + offset)
		elif op == OFFSET:
			if fv:
				return "~"+str(float(val.lstrip("~")) + offset)
			else:
				return "~"+str(int(val.lstrip("~")) + offset)
		elif op == REMOVEDEC:
			return "~"+str(int(float(val.lstrip("~"))))
		elif op == ADDDEC:
			return "~"+str(float(val.lstrip("~")))
	else:
		if op == TORELATIVE:
			if fv:
				return "~"+str(float(val) - offset)
			else:
				return "~"+str(int(val) - offset)
		elif op == TOABSOLUTE:
			return val
		elif op == OFFSET:
			if fv:
				return str(float(val) + offset)
			else:
				return str(int(val) + offset)
		elif op == REMOVEDEC:
			return str(int(float(val)))
		elif op == ADDDEC:
			return str(float(val))

def perform(level, box, options):
	typeval = options["Command Type:"]
	applyto = options["Apply to Coordinate Sets (clone and fill only):"]

	tileEntity = True if options["Operate on:"] == "Command Blocks" else False
	abstorel = options["Coordinate Conversion:"]
	ox = options["X Offset"]
	oy = options["Y Offset"]
	oz = options["Z Offset"]
	if ox == int(ox):
		ox = int(ox)
	if oy == int(oy):
		oy = int(oy)
	if oz == int(oz):
		oz = int(oz)
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities if tileEntity else chunk.Entities:
			if tileEntity:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
			else:
				x = e["Pos"][0].value
				y = e["Pos"][1].value
				z = e["Pos"][2].value
			if (x,y,z) in box:
				if e["id"].value != "Control" and e["id"].value != "MinecartCommandBlock":
					continue
				if "Command" not in e:
					continue
				for type in command_types if typeval == "All" else (typeval,):
					apply = 0
					if type in ("clone","fill","testforblocks"):
						if applyto == "All":
							apply = 7
						elif applyto == "Third (clone, testforblocks dest.)":
							apply = THIRD
						else:
							if "First" in applyto:
								apply |= FIRST
							if "Second" in applyto:
								apply |= SECOND
					typelen = len(type)
					command = e["Command"].value.encode("unicode-escape")
					if command[:typelen].lower() != type and command[:typelen+1].lower() != "/"+type:
						continue
					x1 = y1 = z1 = x2 = y2 = z2 = None
					try:
						if type == "summon" or type == "particle":
							(_, entity, cx, cy, cz, id) = command.split(" ",5)
						elif type == "clone" or type == "testforblocks":
							if len(command.split(" ")) > 10:
								(_, cx, cy, cz, x1, y1, z1, x2, y2, z2, id) = command.split(" ",10)
							else:
								(_, cx, cy, cz, x1, y1, z1, x2, y2, z2) = command.split(" ",9)
								id = ""
						elif type == "fill":
							(_, cx, cy, cz, x1, y1, z1, id) = command.split(" ",7)
						elif type == "playsound":
							(_, sound, player, cx, cy, cz, id) = command.split(" ",6)
						elif type == "spreadplayers":
							cy = "0"
							(_, cx, cz, id) = command.split(" ",3)
						else:
							(_, cx, cy, cz, id) = command.split(" ",4)
					except ValueError:
						print "Command in command block at",x,y,z,"has an incorrect number of parameters.  Skipping."
						continue

					if abstorel == "Absolute Coordinates -> Relative Coordinates":
						if apply == 0 or (apply & FIRST):
							cx = convertValue(cx,x,TORELATIVE)
							cy = convertValue(cy,y,TORELATIVE)
							cz = convertValue(cz,z,TORELATIVE)
						if x1 != None and (apply & SECOND):
							x1 = convertValue(x1,x,TORELATIVE)
							y1 = convertValue(y1,y,TORELATIVE)
							z1 = convertValue(z1,z,TORELATIVE)
						if x2 != None and (apply & THIRD):
							x2 = convertValue(x2,x,TORELATIVE)
							y2 = convertValue(y2,y,TORELATIVE)
							z2 = convertValue(z2,z,TORELATIVE)
					elif abstorel == "Relative Coordinates -> Absolute Coordinates":
						if apply == 0 or (apply & FIRST):
							cx = convertValue(cx,x,TOABSOLUTE)
							cy = convertValue(cy,y,TOABSOLUTE)
							cz = convertValue(cz,z,TOABSOLUTE)
						if x1 != None and (apply & SECOND):
							x1 = convertValue(x1,x,TOABSOLUTE)
							y1 = convertValue(y1,y,TOABSOLUTE)
							z1 = convertValue(z1,z,TOABSOLUTE)
						if x2 != None and (apply & THIRD):
							x2 = convertValue(x2,x,TOABSOLUTE)
							y2 = convertValue(y2,y,TOABSOLUTE)
							z2 = convertValue(z2,z,TOABSOLUTE)
					elif abstorel == "Offset Coordinates":
						if apply == 0 or (apply & FIRST):
							cx = convertValue(cx,ox,OFFSET)
							cy = convertValue(cy,oy,OFFSET)
							cz = convertValue(cz,oz,OFFSET)
						if x1 != None and (apply & SECOND):
							x1 = convertValue(x1,ox,OFFSET)
							y1 = convertValue(y1,oy,OFFSET)
							z1 = convertValue(z1,oz,OFFSET)
						if x2 != None and (apply & THIRD):
							x2 = convertValue(x2,ox,OFFSET)
							y2 = convertValue(y2,oy,OFFSET)
							z2 = convertValue(z2,oz,OFFSET)
					elif abstorel == "Remove Decimal Places":
						if apply == 0 or (apply & FIRST):
							cx = convertValue(cx,0,REMOVEDEC)
							cy = convertValue(cy,0,REMOVEDEC)
							cz = convertValue(cz,0,REMOVEDEC)
						if x1 != None and (apply & SECOND):
							x1 = convertValue(x1,0,REMOVEDEC)
							y1 = convertValue(y1,0,REMOVEDEC)
							z1 = convertValue(z1,0,REMOVEDEC)
						if x2 != None and (apply & THIRD):
							x2 = convertValue(x2,0,REMOVEDEC)
							y2 = convertValue(y2,0,REMOVEDEC)
							z2 = convertValue(z2,0,REMOVEDEC)
					elif abstorel == "Add Decimal Places":
						if apply == 0 or (apply & FIRST):
							cx = convertValue(cx,0,ADDDEC)
							cy = convertValue(cy,0,ADDDEC)
							cz = convertValue(cz,0,ADDDEC)
						if x1 != None and (apply & SECOND):
							x1 = convertValue(x1,0,ADDDEC)
							y1 = convertValue(y1,0,ADDDEC)
							z1 = convertValue(z1,0,ADDDEC)
						if x2 != None and (apply & THIRD):
							x2 = convertValue(x2,0,ADDDEC)
							y2 = convertValue(y2,0,ADDDEC)
							z2 = convertValue(z2,0,ADDDEC)
					
					if type == "summon" or type == "particle":
						e["Command"] = TAG_String(unicode("{} {} {} {} {} {}".format(unicode(type), unicode(entity), unicode(cx), unicode(cy), unicode(cz), unicode(id)).decode("unicode-escape")))
					elif type == "clone" or type == "testforblocks":
						e["Command"] = TAG_String(unicode("{} {} {} {} {} {} {} {} {} {} {}".format(unicode(type), unicode(cx), unicode(cy), unicode(cz), unicode(x1), unicode(y1), unicode(z1), unicode(x2), unicode(y2), unicode(z2), unicode(id)).decode("unicode-escape")))
					elif type == "fill":
						e["Command"] = TAG_String(unicode("{} {} {} {} {} {} {} {}".format(unicode(type), unicode(cx), unicode(cy), unicode(cz), unicode(x1), unicode(y1), unicode(z1), unicode(id)).decode("unicode-escape")))
					elif type == "playsound":
						e["Command"] = TAG_String(unicode("{} {} {} {} {} {} {}".format(unicode(type), unicode(sound), unicode(player), unicode(cx), unicode(cy), unicode(cz), unicode(id)).decode("unicode-escape")))
					elif type == "spreadplayers":
						e["Command"] = TAG_String(unicode("{} {} {} {}".format(unicode(type), unicode(cx), unicode(cz), unicode(id)).decode("unicode-escape")))
					else:
						if type == "testforblock ":
							typef = "testforblock"
						else:
							typef = type
						e["Command"] = TAG_String(unicode("{} {} {} {} {}".format(unicode(typef), unicode(cx), unicode(cy), unicode(cz), unicode(id)).decode("unicode-escape")))
					chunk.dirty = True 
