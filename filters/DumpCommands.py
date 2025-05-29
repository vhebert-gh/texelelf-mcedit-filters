import math
import mcplatform

inputs = (
	("Dump...",("Command Blocks","Command Block Minecarts")),
	("Dump only commands containing: (\"None\" to dump all)",("string","value=None")),
	)

displayName = "Dump Commands"

def perform(level, box, options):
	filterstr = options["Dump only commands containing: (\"None\" to dump all)"]
	if filterstr == "None":
		filtercoms = False
	else:
		filtercoms = True
	tileents = True if options["Dump..."] == "Command Blocks" else False
	commands = []
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
							if filtercoms:
								if e["Command"].value.find(filterstr) != -1:
									commands.append(e["Command"].value + "\n")
							else:
								commands.append(e["Command"].value + "\n")
					else:
						if e["id"].value == "MinecartCommandBlock":
							if filtercoms:
								if e["Command"].value.find(filterstr) != -1:
									commands.append(e["Command"].value + "\n")
							else:
								commands.append(e["Command"].value + "\n")

	text_file = mcplatform.askSaveFile(mcplatform.lastSchematicsDir or mcplatform.schematicsDir, "Save Dumped Text File...", "", "Text File\0*.txt\0\0", ".txt")
	if text_file == None:
		print "ERROR: No filename provided!"
		return
	file = open(text_file,"w")
	file.writelines(commands)
	file.close()
