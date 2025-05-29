import os
import glob
from copy import deepcopy
from pymclevel.materials import alphaMaterials
from pymclevel import nbt, TAG_Compound, TAG_List, TAG_Int, TAG_Byte_Array, TAG_Short, TAG_Byte, TAG_String, TAG_Double, TAG_Float
from pymclevel import BoundingBox, saveFileDir
import mcplatform
import pygame
import numpy
import math

displayName = "Batch Map It!"

inputs = (
	("Thanks go to gentlegiantJGC (https://twitter.com/gentlegiantJGC) for an updated color palette!","label"),
	("Transparency Mode:",("None","Use Default Color (#FF00FF)","User-Specified Color Below")),
	("Transparency Color:",("string","value=#FF00FF")),
	("Use Nearest-Color Transparency (recommended for lossy image formats):",False),
	("Image path:",("string","value=None")),
	)
	
map_palette = {
	(88,124,39):4,(108,151,47):5,(125,176,55):6,(66,93,29):7,(172,162,114):8,(210,199,138):9,(244,230,161):10,
	(128,122,85):11,(138,138,138):12,(169,169,169):13,(197,197,197):14,(104,104,104):15,(178,0,0):16,(217,0,0):17,
	(252,0,0):18,(133,0,0):19,(111,111,178):20,(136,136,217):21,(158,158,252):22,(83,83,133):23,(116,116,116):24,
	(142,142,142):25,(165,165,165):26,(87,87,87):27,(0,86,0):28,(0,105,0):29,(0,123,0):30,(0,64,0):31,(178,178,178):32,
	(217,217,217):33,(252,252,252):34,(133,133,133):35,(114,117,127):36,(139,142,156):37,(162,166,182):38,(85,87,96):39,
	(105,75,53):40,(128,93,65):41,(149,108,76):42,(78,56,39):43,(78,78,78):44,(95,95,95):45,(111,111,111):46,(58,58,58):47,
	(44,44,178):48,(54,54,217):49,(63,63,252):50,(33,33,133):51,(99,83,49):52,(122,101,61):53,(141,118,71):54,(74,62,38):55,
	(178,175,170):56,(217,214,208):57,(252,249,242):58,(133,131,127):59,(150,88,36):60,(184,108,43):61,(213,125,50):62,
	(113,66,27):63,(124,52,150):64,(151,64,184):65,(176,75,213):66,(93,39,113):67,(71,107,150):68,(87,130,184):69,(101,151,213):70,
	(53,80,113):71,(159,159,36):72,(195,195,43):73,(226,226,50):74,(120,120,27):75,(88,142,17):76,(108,174,21):77,(125,202,25):78,
	(66,107,13):79,(168,88,115):80,(206,108,140):81,(239,125,163):82,(126,66,86):83,(52,52,52):84,(64,64,64):85,(75,75,75):86,
	(39,39,39):87,(107,107,107):88,(130,130,130):89,(151,151,151):90,(80,80,80):91,(52,88,107):92,(64,108,130):93,(75,125,151):94,
	(39,66,80):95,(88,43,124):96,(108,53,151):97,(125,62,176):98,(66,33,93):99,(36,52,124):100,(43,64,151):101,(50,75,176):102,
	(27,39,93):103,(71,52,36):104,(87,64,43):105,(101,75,50):106,(53,39,27):107,(71,88,36):108,(87,108,43):109,(101,125,50):110,
	(53,66,27):111,(107,36,36):112,(130,43,43):113,(151,50,50):114,(80,27,27):115,(17,17,17):116,(21,21,21):117,(25,25,25):118,
	(13,13,13):119,(174,166,53):120,(212,203,65):121,(247,235,76):122,(130,125,39):123,(63,152,148):124,(78,186,181):125,
	(91,216,210):126,(47,114,111):127,(51,89,178):128,(62,109,217):129,(73,129,252):130,(39,66,133):131,(0,151,39):132,(0,185,49):133,
	(0,214,57):134,(0,113,30):135,(90,59,34):136,(110,73,41):137,(127,85,48):138,(67,44,25):139,(78,1,0):140,(95,1,0):141,(111,2,0):142,(58,1,0):143,
	}

mapkeys = map_palette.keys()
cache = deepcopy(map_palette)

filetypes = ("*.gif","*.jpg","*.tga","*.png","*.jpeg","*.bmp","*.tif","*.pcx")

def FindClosestPaletteIndex(r,g,b,trans,nearest):
	if not nearest and trans != None:
		if (r,g,b) == trans:
			return 0
		
	distance = float("inf")
	pal = None
	for (pr, pg, pb) in mapkeys:
		newdist = (pr - r)**2 + (pg - g)**2 + (pb - b)**2
		if newdist <= distance:
			distance = newdist
			pal = (pr, pg, pb)
	else:
		if nearest and trans != None:
			ar, ag, ab = trans
			newdist = (ar - r)**2 + (ag - g)**2 + (ab - b)**2
			if newdist <= distance:
				cache[(r,g,b)] = 0
				return 0
		
	if pal == None:
		return 0
	ind = map_palette[pal]
	cache[(r,g,b)] = ind
	return ind

def CreateNewMapFile(path, number, colors):
	map = TAG_Compound()
	map["data"] = TAG_Compound()
	map["data"]["scale"] = TAG_Byte(4)
	map["data"]["dimension"] = TAG_Byte(0)
	map["data"]["height"] = TAG_Short(128)
	map["data"]["width"] = TAG_Short(128)
	map["data"]["xCenter"] = TAG_Int(2147483647)
	map["data"]["yCenter"] = TAG_Int(2147483647)
	map["data"]["colors"] = TAG_Byte_Array(colors)
	map.save(os.path.join(path,"map_"+str(number)+".dat"))
	
def perform(level, box, options):
	imgpath = options["Image path:"]
	nearest = options["Use Nearest-Color Transparency (recommended for lossy image formats):"]
	tmode = options["Transparency Mode:"]
	tcolor = options["Transparency Color:"]
	if tmode == "Use Default Color (#FF00FF)":
		transparent = (255,0,255)
	elif tmode == "User-Specified Color Below":
		if tcolor[0] == "#":
			alphacolor = int(tcolor[1:7],16)
			transparent = (alphacolor>>16,(alphacolor>>8)&0xff,alphacolor&0xff)
		else:
			raise Exception("ERROR! The provided transparency color was formatted incorrectly! Colors must in hexadecimal format, in the form #RRGGBB")
	else:
		transparent = None

	if level.dimNo:
		datafolder = level.parentWorld.worldFolder.getFolderPath("data")	
	else:
		datafolder = level.worldFolder.getFolderPath("data")

	if not os.path.exists(datafolder):
		try:
			os.makedirs(datafolder)
		except:
			raise OSError("ERROR! Data folder does not exist and could not be created. Please create a \"data\" folder at: "+datafolder)

	idcountpath = os.path.join(datafolder,"idcounts.dat")
	global idcount
	idcount	= 0
	if os.path.exists(idcountpath):
		idcountfile = nbt.load(idcountpath)
		if "map" in idcountfile:
			idcount = idcountfile["map"].value
		else:
			idcount = 0
			idcountfile["map"] = TAG_Short(0)
	else:
		idcount = 0
		idcountfile = TAG_Compound()
		idcountfile["map"] = TAG_Short(0)

	if imgpath != "None":
		if os.path.exists(imgpath):
			image_path = imgpath
		else:
			image_path = mcplatform.askOpenFile(title="Select an image from the target folder", schematics=False)
	else:
		image_path = mcplatform.askOpenFile(title="Select an image from the target folder", schematics=False)

	if image_path == None:
		raise Exception("ERROR: No path provided!")

	image_path, _ = os.path.split(image_path)
		
	files = []
	for ftypes in filetypes:
		files.extend(glob.glob(os.path.join(image_path,ftypes)))
	files.sort()

	def processFiles(file_list, result):
		def processImage(image):
			global idcount
			surface = pygame.image.load(image)
			(height, width) = surface.get_size()
			
			sx, sy, sz = box.size
			xsize, ysize, zsize = box.size * 128
			loopx = int(math.ceil(float(width)/128.0))
			loopy = int(math.ceil(float(height)/128.0))
			
			if (loopx*loopy)+idcount > 65535:
				raise Exception("\nERROR! There are not enough maps left for this world.\n"
				"Only 65,535 map files are allowed per world, and there are "+str(idcount)+" maps in this world.")
				return

			image = numpy.fromstring(pygame.image.tostring(surface, "RGB"),dtype=numpy.uint8).reshape(width,height,3)
			progresscount = 1
			progressmax = loopx * loopy
			startid = idcount + 1
			for lx in xrange(loopx):
				for ly in xrange(loopy):
					progresscount += 1
					idcount += 1
					converted = numpy.zeros((128,128),dtype=numpy.uint8)
					offsetx = lx * 128
					offsety = ly * 128
					for x in xrange(128):
						for y in xrange(128):
							if (offsetx+x) >= width:
								break
							elif(offsety+y) >= height:
								break
							r,g,b = (image[offsetx+x,offsety+y,0],image[offsetx+x,offsety+y,1],image[offsetx+x,offsety+y,2])
							if (r,g,b) in cache:
								converted[x,y] = cache[(r,g,b)]
							else:
								converted[x,y] = FindClosestPaletteIndex(r,g,b,transparent,nearest)
						if(offsetx+x) >= width:
							break
					CreateNewMapFile(datafolder, idcount, converted)
			idcountfile["map"] = TAG_Short(idcount)
			idcountfile.save(idcountpath, compressed=False)

		count = 0
		for image in file_list:
			idbefore = idcount
			processImage(image)
			ids = ";".join([str(a) for a in range(idbefore+1,idcount+1)])
			result.append(image+","+ids+",/give @a minecraft:filled_map 64 "+str(ids)+"\n")
			yield count, len(file_list), image
			count += 1

	result = ["Image,Map ID(s),Give Command\n",]
	level.showProgress("Batch processing folder:", processFiles(files, result))

	f = open(os.path.join(datafolder,"results.csv"),"w")
	f.writelines(result)
	f.close()

	raise Exception("Finished processing folder")
