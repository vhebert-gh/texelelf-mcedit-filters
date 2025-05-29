from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float
from copy import deepcopy
import math

displayName = "Command Block to Minecart Command Block"
inputs = (
	("Operation:",("Command Blocks -> Minecart Command Blocks","Minecart Command Blocks -> Command Blocks")),
	)

def perform(level, box, options):
	tileents = True if options["Operation:"] == "Command Blocks -> Minecart Command Blocks" else False
	entsToAdd = []
	entsToDelete = []
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities if tileents else chunk.Entities:
			if tileents:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
			else:
				x = int(math.floor(e["Pos"][0].value))
				y = int(math.floor(e["Pos"][1].value))
				z = int(math.floor(e["Pos"][2].value))
			if (x,y,z) in box:
				if tileents:
					if e["id"].value == "Control":
						newcommand = TAG_Compound()
						newcommand["id"] = TAG_String("MinecartCommandBlock")
						newcommand["Fire"] = TAG_Short(-1)
						newcommand["OnGround"] = TAG_Byte(0)
						newcommand["FallDistance"] = TAG_Float(0.0)
						newcommand["Rotation"] = TAG_List([TAG_Float(0.0),TAG_Float(0.0)])
						newcommand["Motion"] = TAG_List([TAG_Double(0.0),TAG_Double(0.0),TAG_Double(0.0)])
						newcommand["Command"] = e["Command"]
						newcommand["CustomName"] = e["CustomName"]
						newcommand["Pos"] = TAG_List([TAG_Double(float(x)+0.5),TAG_Double(float(y)+0.5),TAG_Double(float(z)+0.5)])
						level.setBlockAt(x, y, z, 0)
						level.setBlockDataAt(x, y, z, 0)
						entsToAdd.append((chunk,newcommand))
						entsToDelete.append((chunk, e))
				else:
					if e["id"].value == "MinecartCommandBlock":
						newcommand = TAG_Compound()
						newcommand["id"] = TAG_String("Control")
						newcommand["x"] = TAG_Int(x)
						newcommand["y"] = TAG_Int(y)
						newcommand["z"] = TAG_Int(z)
						newcommand["Command"] = e["Command"]
						newcommand["CustomName"] = e["CustomName"]
						level.setBlockAt(x, y, z, 137)
						level.setBlockDataAt(x, y, z, 0)
						entsToAdd.append((chunk,newcommand))
						entsToDelete.append((chunk, e))

	for (chunk, entity) in entsToAdd:
		if not tileents:
			chunk.TileEntities.append(entity)
		else:
			chunk.Entities.append(entity)
		chunk.dirty = True
				
	for (chunk, entity) in entsToDelete:
		if tileents:
			chunk.TileEntities.remove(entity)
		else:
			chunk.Entities.remove(entity)
		chunk.dirty = True


