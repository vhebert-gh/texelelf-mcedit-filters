import re
from pymclevel import TAG_String, TAG_List, TAG_Compound, TAG_Float, TAG_Double, TAG_Byte, TAG_Short
from pymclevel import TileEntity
import math

displayName = "Edit Command Block"

sectional = "\xA7"
newline = "\n"

inputs = [
	(("Operate Against:",("Command Blocks","Minecart Command Blocks","Signs")),
	("Operation:",("Set Command","Set Name","Set Command and Name","Create New Command Blocks","Replace String","Apply Auto Scoreboard")),
	("Sectional Character Substitute",("string","value=%%")),
	("Newline Sequence",("string","value=%%n")),
	("Step Sequence",("string","value=##")),
	("Name:",("string","value=None","width=700")),
	("Command:",("string","value=None","width=700")),
	("Step Start:",0),
	("Step Increment:",0),
	("Primary Increment Order:",("Y","X","Z")),
	("Secondary Increment Order:",("X","Z","Y")),
	("Tertiary Increment Order:",("Z","Y","X")),
	("Set and Create","title")),
	
	(("Replace Operation:",("Simple String Replace","Regular Expression Replace")),
	("Operate On:",("Commands","Names","Both")),
	("Find:",("string","value=None","width=700")),
	("Replace With:",("string","value=None","width=700")),
	("For a basic reference on Regular Expressions, please visit:\nhttp://www.regular-expressions.info/reference.html\nor:\nhttp://msdn.microsoft.com/en-us/library/az24scfc.aspx","label"),
	("Case-insensitive Regular Expression",False),
	("Multi-line Regular Expression",False),
	("Dot ( . ) can match Newlines",False),
	("Replace","title")),
	
	(("Set:",("All","SuccessCountName","SuccessCountObjective","AffectedBlocksName","AffectedBlocksObjective",
					"AffectedEntitiesName","AffectedEntitiesObjective","AffectedItemsName","AffectedItemsObjective")),
	("SuccessCountName",("string","value=None")),
	("SuccessCountObjective",("string","value=None")),
	("AffectedBlocksName",("string","value=None")),
	("AffectedBlocksObjective",("string","value=None")),
	("AffectedEntitiesName",("string","value=None")),
	("AffectedEntitiesObjective",("string","value=None")),
	("AffectedItemsName",("string","value=None")),
	("AffectedItemsObjective",("string","value=None")),
	("Auto Scoreboard","title")),
	
	]

def InsertSpecial(stringval,newlineseq,sec):
	if stringval.upper() == "NONE":
		return ""
	commandstring = stringval.encode("unicode-escape")
	commandstring = commandstring.replace(str(newlineseq),newline)
	commandstring = commandstring.replace(str(sec),sectional)
	commandstring = commandstring.decode("unicode-escape")
	return commandstring

def perform(level, box, options):
	opagainst = options["Operate Against:"]
	op = options["Operation:"]
	replaceop = options["Replace Operation:"]
	opon = options["Operate On:"]
	priorder = options["Primary Increment Order:"]
	secorder = options["Secondary Increment Order:"]
	terorder = options["Tertiary Increment Order:"]
	newblock = True if op == "Create New Command Blocks" else False
	standinchar = options["Sectional Character Substitute"]
	newlineseq = options["Newline Sequence"]
	stepseq = options["Step Sequence"]
	step = options["Step Start:"]
	incr = options["Step Increment:"]
	
	scoreset = options["Set:"]
	SuccessCountName = InsertSpecial(options["SuccessCountName"],newlineseq,standinchar)
	SuccessCountObjective = InsertSpecial(options["SuccessCountObjective"],newlineseq,standinchar)
	AffectedBlocksName = InsertSpecial(options["AffectedBlocksName"],newlineseq,standinchar)
	AffectedBlocksObjective = InsertSpecial(options["AffectedBlocksObjective"],newlineseq,standinchar)
	AffectedEntitiesName = InsertSpecial(options["AffectedEntitiesName"],newlineseq,standinchar)
	AffectedEntitiesObjective = InsertSpecial(options["AffectedEntitiesObjective"],newlineseq,standinchar)
	AffectedItemsName = InsertSpecial(options["AffectedItemsName"],newlineseq,standinchar)
	AffectedItemsObjective = InsertSpecial(options["AffectedItemsObjective"],newlineseq,standinchar)
	
	case = re.IGNORECASE if options["Case-insensitive Regular Expression"] else 0
	multiline = re.MULTILINE if options["Multi-line Regular Expression"] else 0
	dot = re.DOTALL if options["Dot ( . ) can match Newlines"] else 0
	
	commandstring = InsertSpecial(options["Command:"],newlineseq,standinchar)
	namestring = InsertSpecial(options["Name:"],newlineseq,standinchar)
	findstring = InsertSpecial(options["Find:"],newlineseq,standinchar)
	replacestring = InsertSpecial(options["Replace With:"],newlineseq,standinchar)

	if replacestring == "None" or replacestring == "":
		replacestring = ""

	if replacestring.find(stepseq) != -1:
		doincrement = True
	else:
		doincrement = False

	blocklist = []
	for (chunk, _, _) in level.getChunkSlices(box):
		if newblock:
			if opagainst == "Signs":
				raise Exception("\nThe operation specified is incompabile with Signs")
			(cx,cz) = chunk.chunkPosition
			cposx = cx * 16
			cposz = cz * 16
			for y in range(box.miny,box.maxy,1):
				for x in range((cposx if (cposx > box.minx) else box.minx),(cposx+16 if ((cposx+16) < box.maxx) else box.maxx),1):
					for z in range((cposz if (cposz > box.minz) else box.minz),(cposz+16 if((cposz+16) < box.maxz) else box.maxz),1):
						if opagainst == "Command Blocks":
							level.setBlockAt(x, y, z, 137)
							e = TileEntity.Create("Control")
							e["Command"] = TAG_String()
							TileEntity.setpos(e, (x, y, z))
							chunk.TileEntities.append(e)
						else:
							e = TAG_Compound()
							e["id"] = TAG_String("MinecartCommandBlock")
							e["Fire"] = TAG_Short(-1)
							e["OnGround"] = TAG_Byte(0)
							e["FallDistance"] = TAG_Float(0.0)
							e["Rotation"] = TAG_List([TAG_Float(0.0),TAG_Float(0.0)])
							e["Motion"] = TAG_List([TAG_Double(0.0),TAG_Double(0.0),TAG_Double(0.0)])
							e["Command"] = TAG_String()
							e["CustomName"] = TAG_String("@")
							e["Pos"] = TAG_List([TAG_Double(float(x)+0.5),TAG_Double(float(y)+0.5),TAG_Double(float(z)+0.5)])
							chunk.Entities.append(e)
			chunk.dirty = True
		for e in chunk.TileEntities if (opagainst == "Command Blocks" or opagainst == "Signs") else chunk.Entities:
			if opagainst == "Command Blocks" or opagainst == "Signs":
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if opagainst == "Signs":
					entity_name = "Sign"
				else:
					entity_name = "Control"
			else:
				x = int(math.floor(e["Pos"][0].value))
				y = int(math.floor(e["Pos"][1].value))
				z = int(math.floor(e["Pos"][2].value))
				entity_name = "MinecartCommandBlock"
			if (x,y,z) in box:
				if e["id"].value == entity_name:
					blocklist.append([x,y,z,e,chunk])

	if priorder == "X":
		pri = 2
	elif priorder == "Y":
		pri = 1
	elif priorder == "Z":
		pri = 0

	if secorder == "X":
		sec = 2
	elif secorder == "Y":
		sec = 1
	elif secorder == "Z":
		sec = 0

	if terorder == "X":
		ter = 2
	elif terorder == "Y":
		ter = 1
	elif terorder == "Z":
		ter = 0

	blocklist.sort(key=lambda s: (s[pri], s[sec], s[ter]))
	
	for (x, y, z, e, chunk) in blocklist:
		if op == "Replace String":
			if replaceop == "Simple String Replace":
				if entity_name == "Sign":
					for n in range(1,5):
						if "Text"+str(n) in e:
							newstring = e["Text"+str(n)].value
							if newstring.find(findstring) != -1:
								if doincrement:
									newstr = unicode.replace(replacestring,stepseq,str(step))
									step += incr
									newstring = unicode.replace(newstring,findstring,newstr)
									e["Text"+str(n)] = TAG_String(newstring)
									chunk.dirty = True
								else:
									newstring = unicode.replace(newstring,findstring,replacestring)
									e["Text"+str(n)] = TAG_String(newstring)
									chunk.dirty = True
				else:
					if opon == "Commands" or opon == "Both":
						if "Command" in e:
							newstring = e["Command"].value
							if newstring.find(findstring) != -1:
								if doincrement:
									newstr = unicode.replace(replacestring,stepseq,str(step))
									step += incr
									newstring = unicode.replace(newstring,findstring,newstr)
									e["Command"] = TAG_String(newstring)
									chunk.dirty = True
								else:
									newstring = unicode.replace(newstring,findstring,replacestring)
									e["Command"] = TAG_String(newstring)
									chunk.dirty = True
					if opon == "Names" or opon == "Both":
						if "CustomName" in e:
							newstring = e["CustomName"].value
							if newstring.find(findstring) != -1:
								if doincrement:
									newstr = unicode.replace(replacestring,stepseq,str(step))
									step += incr
									newstring = unicode.replace(newstring,findstring,newstr)
									e["CustomName"] = TAG_String(newstring)
									chunk.dirty = True
								else:
									newstring = unicode.replace(newstring,findstring,replacestring)
									e["CustomName"] = TAG_String(newstring)
									chunk.dirty = True
			elif replaceop == "Regular Expression Replace":
				if entity_name == "Sign":
					for n in range(1,5):
						if "Text"+str(n) in e:
							newstring = e["Text"+str(n)].value
							if doincrement:
								newstr = unicode.replace(replacestring,stepseq,str(step))
								step += incr
								newstring = re.sub(findstring,newstr, newstring,flags=re.UNICODE | case | multiline | dot)
								e["Text"+str(n)] = TAG_String(newstring)
								chunk.dirty = True
							else:
								newstring = re.sub(findstring,replacestring, newstring,flags=re.UNICODE | case | multiline | dot)
								e["Text"+str(n)] = TAG_String(newstring)
								chunk.dirty = True
				else:
					if opon == "Commands" or opon == "Both":
						if "Command" in e:
							newstring = e["Command"].value
							if doincrement:
								newstr = unicode.replace(replacestring,stepseq,str(step))
								step += incr
								newstring = re.sub(findstring,newstr, newstring,flags=re.UNICODE | case | multiline | dot)
								e["Command"] = TAG_String(newstring)
								chunk.dirty = True
							else:
								newstring = re.sub(findstring,replacestring, newstring,flags=re.UNICODE | case | multiline | dot)
								e["Command"] = TAG_String(newstring)
								chunk.dirty = True
					if opon == "Names" or opon == "Both":
						if "CustomName" in e:
							newstring = e["CustomName"].value
							if doincrement:
								newstr = unicode.replace(replacestring,stepseq,str(step))
								step += incr
								newstring = re.sub(findstring,newstr, newstring,flags=re.UNICODE | case | multiline | dot)
								e["CustomName"] = TAG_String(newstring)
								chunk.dirty = True
							else:
								newstring = re.sub(findstring,replacestring, newstring,flags=re.UNICODE | case | multiline | dot)
								e["CustomName"] = TAG_String(newstring)
								chunk.dirty = True
		elif op == "Apply Auto Scoreboard":
			if entity_name == "Sign":
				raise Exception("\nThe operation specified is incompabile with Signs")
			if scoreset == "All" or scoreset == "SuccessCountName":
				e["SuccessCountName"] = TAG_String(SuccessCountName)
			if scoreset == "All" or scoreset == "SuccessCountObjective":
				e["SuccessCountObjective"] = TAG_String(SuccessCountObjective)
			if scoreset == "All" or scoreset == "AffectedBlocksName":
				e["AffectedBlocksName"] = TAG_String(AffectedBlocksName)
			if scoreset == "All" or scoreset == "AffectedBlocksObjective":
				e["AffectedBlocksObjective"] = TAG_String(AffectedBlocksObjective)
			if scoreset == "All" or scoreset == "AffectedEntitiesName":
				e["AffectedEntitiesName"] = TAG_String(AffectedEntitiesName)
			if scoreset == "All" or scoreset == "AffectedEntitiesObjective":
				e["AffectedEntitiesObjective"] = TAG_String(AffectedEntitiesObjective)
			if scoreset == "All" or scoreset == "AffectedItemsName":
				e["AffectedItemsName"] = TAG_String(AffectedItemsName)
			if scoreset == "All" or scoreset == "AffectedItemsObjective":
				e["AffectedItemsObjective"] = TAG_String(AffectedItemsObjective)
			chunk.dirty = True
		else:
			if entity_name == "Sign":
				raise Exception("\nThe operation specified is incompabile with Signs")
			if op == "Set Command" or op == "Set Command and Name" or newblock:
				if commandstring != "" and commandstring != "None":
					if commandstring.find(stepseq) != -1:
						newstr = unicode.replace(commandstring,stepseq,str(step))
						step += incr
						e["Command"] = TAG_String(newstr)
						chunk.dirty = True
					else:
						e["Command"] = TAG_String(commandstring)
						chunk.dirty = True
			if op == "Set Name" or op == "Set Command and Name" or newblock:
				if namestring != "" and namestring != "None":
					if namestring.find(stepseq) != -1:
						newstr = unicode.replace(namestring,stepseq,str(step))
						step += incr
						e["CustomName"] = TAG_String(newstr)
						chunk.dirty = True
					else:
						e["CustomName"] = TAG_String(namestring)
						chunk.dirty = True
