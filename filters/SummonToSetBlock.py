from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float
from copy import deepcopy
import re

displayName = "Summon to SetBlock"

inputs = ( ("Method:",("replace","keep","destroy","Time Auto-detect")),)

def ParseFallingSand(meta):
	ind = meta.find("TileEntityData")
	if ind == -1:
		metadata = ""
	else:
		bracecount = 1
		lastind = -1
		for i in xrange(ind+16, len(meta)):
			if meta[i] == "{":
				bracecount += 1
			elif meta[i] == "}":
				bracecount -= 1
			if bracecount == 0:
				lastind = i+1
				break
		else:
			print "Error parsing the metadata!"
		metadata = meta[ind+15:lastind]
		meta = meta[:ind] + meta[lastind:]
	temp = meta.split(",")
	pairs = {}
	for p in temp:
		if p != "":
			key, val = p.partition(":")[::2]
			pairs[key] = val

	dec = re.compile(r"[^\d.]+")
			
	if "TileID" not in pairs:
		if "Tile" in pairs:
			id = re.sub(dec,"",pairs["Tile"])
		else:
			id = 12
	else:
		id = re.sub(dec,"",pairs["TileID"])

	if "Time" in pairs:
		time = re.sub(dec,"",pairs["Time"])
	else:
		time = 0

	if "Data" in pairs:
		data = re.sub(dec,"",pairs["Data"])
	else:
		data = 0

	return((id, data, time, metadata))

def perform(level, box, options):
	meth = options["Method:"]
	for (chunk, _, _) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:

				if e["id"].value != "Control":
					continue

				if "Command" not in e:
					continue

				try:
					(_, type, cx, cy, cz, metadata) = e["Command"].value.split(" ",5)
				except ValueError:
					continue

				if type != "FallingSand":
					continue
					
				if cx[0] == "~":
					cx = "~"+str(int(float(cx[1:])))
				else:
					cx = int(float(cx))

				if cy[0] == "~":
					cy = "~"+str(int(float(cy[1:])))
				else:
					cy = int(float(cy))

				if cz[0] == "~":
					cz = "~"+str(int(float(cz[1:])))
				else:
					cz = int(float(cz))

					
				if metadata == "":
					id = 12
					data = 0
					time = 0
					mdata = ""
				else:
					(id, data, time, mdata) = ParseFallingSand(metadata)

				if meth == "Time Auto-detect":
					if int(time) == 0:
						method = "destroy"
					else:
						method = "replace"
				else:
					method = meth

				e["Command"] = TAG_String(unicode("setblock {} {} {} {} {} {} {}".format(unicode(cx), unicode(cy), unicode(cz), unicode(id), unicode(data), unicode(method), unicode(mdata)).decode("unicode-escape")))
				chunk.dirty = True	