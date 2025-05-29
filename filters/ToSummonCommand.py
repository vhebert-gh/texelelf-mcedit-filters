from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float, TAG_Long, TAG_Byte_Array, TAG_Int_Array
from pymclevel import MCSchematic
import math
import inspect
from copy import deepcopy

displayName = "To Summon Command"

inputs = (
			("Command Type:",("summon","testfor")),
			("Testfor detection type:",("Global","Global with Radius","Sphere Region","Box Region")),
			("Sphere radius maximum (-1 to ignore):",1),
			("Sphere radius minimum (-1 to ignore):",-1),
			("Box dimensions (XxYxZ):",("string","value=1x1x1")),
			("Testfor count (-1 to ignore):",-1),
		)

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
	editor = inspect.stack()[1][0].f_locals.get('self', None).editor

	summon = True if options["Command Type:"] == "summon" else False
	testfortype = options["Testfor detection type:"]
	radmax = options["Sphere radius maximum (-1 to ignore):"]
	radmin = options["Sphere radius minimum (-1 to ignore):"]
	bx, by, bz = options["Box dimensions (XxYxZ):"].split("x")
	bx = int(bx)
	by = int(by)
	bz = int(bz)
	count = options["Testfor count (-1 to ignore):"]
	
	ents = level.getEntitiesInBox(box)
	dimensions = int(math.ceil(len(ents) ** (1.0/3.0)))
	schematic = MCSchematic((dimensions, dimensions, dimensions), mats=level.materials)
	xCtr = yCtr = zCtr = 0
	for e in ents:
		ent = deepcopy(e)
		type = ent["id"].value
		x = ent["Pos"][0].value
		y = ent["Pos"][1].value
		z = ent["Pos"][2].value
		if summon:
			if x == int(x)+0.5:
				x = str(int(x))
			else:
				x = "%.4f" % x
			if y == int(y)+0.5:
				y = str(int(y))
			else:
				y = "%.4f" % y
			if z == int(z)+0.5:
				z = str(int(z))
			else:
				z = "%.4f" % z
		else:
			x = int(x)
			y = int(y)
			x = int(z)
		del ent["id"]
		del ent["Pos"]
		mdata = "{"+NBT2Command(ent)+"}"

		if summon:
			command = unicode("summon {} {} {} {} {}".format(unicode(type),unicode(x), unicode(y), unicode(z), unicode(mdata)).decode("unicode-escape"))
		else:
			selector = "@e[type="+type
			if testfortype == "Global":
				if count > -1:
					if selector:
						selector += ","
					selector += "c="+str(count)
			elif testfortype == "Global with Radius":
				if radmax > -1:
					if selector:
						selector += ","
					selector += "r="+str(radmax)
				if radmin > -1:
					if selector:
						selector += ","
					selector += "rm="+str(radmin)
				if count > -1:
					if selector:
						selector += ","
					selector += "c="+str(count)
			elif testfortype == "Sphere Region":
				selector += ",x="+str(x)+",y="+str(y)+",z="+str(z)
				if radmax > -1:
					if selector:
						selector += ","
					selector += "r="+str(radmax)
				if radmin > -1:
					if selector:
						selector += ","
					selector += "rm="+str(radmin)
				if count > -1:
					if selector:
						selector += ","
					selector += "c="+str(count)
			else:
				if selector:
					selector += ","
				selector += "x="+str(int(x-(bx/2)))+",y="+str(int(y-(by/2)))+",z="+str(int(z-(bz/2)))
				selector += "dx="+str(int(math.ceil(bx/2.0)-1))+",dy="+str(int(math.ceil(by/2.0)-1))+",dz="+str(int(math.ceil(bz/2.0)-1))
				if count > -1:
					if selector:
						selector += ","
					selector += "c="+str(count)
			selector += "]"
			command = unicode("testfor {} {}".format(unicode(selector), unicode(mdata)).decode("unicode-escape"))		
		schematic.setBlockAt(xCtr, yCtr, zCtr, 137)
		schematic.setBlockDataAt(xCtr, yCtr, zCtr, 0)
		schematic.TileEntities.append(CommandBlock(xCtr,yCtr,zCtr,command))
		xCtr += 1
		if xCtr >= dimensions:
			xCtr = 0
			zCtr += 1
		if zCtr >= dimensions:
			zCtr = 0
			yCtr += 1

	editor.addCopiedSchematic(schematic)
	raise Exception("Schematic successfully added to clipboard.")
