from pymclevel import TAG_Byte, TAG_Short, TAG_Int, TAG_Compound, TAG_List, TAG_String, TAG_Double, TAG_Float
from pymclevel import BoundingBox
from copy import deepcopy

displayName = "Jigarbov's Control Filter"

inputs = (("Positioning:",("Relative","Absolute")),
	("X",0),
	("Y",0),
	("Z",0),
	)

def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def perform(level, box, options):
	pos = options["Positioning:"]
	ox = options["X"]
	oy = options["Y"]
	oz = options["Z"]
	
	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:
				if e["id"].value != "Control":
					continue
				if "Command" not in e:
					continue

				command = e["Command"].value
				temp = command.split(" ")
				for t in temp:
					if t[0] == "@":
						params = t[3:-1]
						break
				else:
					continue

				if pos == "Relative":
					cx = x + ox
					cy = y + oy
					cz = z + oz
				else:
					cx = ox
					cy = oy
					cz = oz
					
				indx = indy = indz = None
				paramlist = params.split(",")
				for p in paramlist:
					if "x=" in p:
						indx = paramlist.index(p)
					elif "y=" in p:
						indy = paramlist.index(p)
					elif "z=" in p:
						indz = paramlist.index(p)
				if indx != None:
					paramlist[indx] = paramlist[indx][:2] + str(cx)
				if indy != None:
					paramlist[indy] = paramlist[indy][:2] + str(cy)
				if indz != None:
					paramlist[indz] = paramlist[indz][:2] + str(cz)

				for c in xrange(3):
					if not is_num(paramlist[c]):
						break
					if c == 0:
						paramlist[c] = str(cx)
					elif c == 1:
						paramlist[c] = str(cy)
					elif c == 2:
						paramlist[c] = str(cz)
					
				newstr = None
				for t in temp:
					if t[0] == "@":
						ind = temp.index(t)
						newstr = t[:3] + (",".join(paramlist)) + t[-1:]
						break
				if newstr != None:
					temp[ind] = newstr

				e["Command"] = TAG_String(" ".join(temp))
				chunk.dirty = True