from random import randrange
from pymclevel.materials import alphaMaterials

displayName = "Jigarbov's Drippy Noise Filter"
	
inputs = (
	("Operation:", ("Noise", "Noise Field","Melt","Draw Compass")),
	("Direction:", ("Upward (+Y)","Downward (-Y)","Eastward (+X)","Westward (-X)","Southward (+Z)","Northward (-Z)")),
	("Drip Block (air if none)", alphaMaterials.Air),
	("Drip Block is cloned from peak block",False),
	("Percent Peaks",30.0),
	("Percent Peaks Drippy",20.0),
	("Drip space gap",5),
	("Max drips per drip",2),
	("Percent Low Peak Height",33.0),
	("Percent Medium Peak Height",33.0),
	("Percent High Peak Height",33.0),
	("Block Filter", ("Ignore","Extend Only","Do Not Extend")),
	("Filter Block 1", alphaMaterials.Air),
	("Filter Block 2", alphaMaterials.Air),
	("Filter Block 3", alphaMaterials.Air),
	)

def perform(level, box, options):

	op = options["Operation:"]
	dripblock = options["Drip Block (air if none)"]
	percentage = options["Percent Peaks"]
	drippypercent = options["Percent Peaks Drippy"]
	drippynum = options["Max drips per drip"]
	dripspace = options["Drip space gap"]
	dripclone = options["Drip Block is cloned from peak block"]
	
	filterop = options["Block Filter"]
	block1 = options["Filter Block 1"]
	block2 = options["Filter Block 2"]
	block3 = options["Filter Block 3"]	
	
	perlow = options["Percent Low Peak Height"]
	permed = options["Percent Medium Peak Height"]
	perhigh = options["Percent High Peak Height"]
	
	randnumlist = []
	filterblock = []
	filterblock.append((block1.ID,block1.blockData))
	if block2.ID != 0:
		filterblock.append((block2.ID,block2.blockData))
	if block3.ID != 0:
		filterblock.append((block3.ID,block3.blockData))
		
	dx = 1 if options["Direction:"] == "Eastward (+X)" else -1 if options["Direction:"] == "Westward (-X)" else 0
	dy = 1 if options["Direction:"] == "Upward (+Y)" else -1 if options["Direction:"] == "Downward (-Y)" else 0
	dz = 1 if options["Direction:"] == "Southward (+Z)" else -1 if options["Direction:"] == "Northward (-Z)" else 0

	if dx:
		length = box.maxx-box.minx
		if dripblock.ID != 0 or dripclone:
			length -= dripspace
	elif dy:
		length = box.maxy-box.miny
		if dripblock.ID != 0 or dripclone:
			length -= dripspace
	elif dz:
		length = box.maxz-box.minz
		if dripblock.ID != 0 or dripclone:
			length -= dripspace

	def GraduatedLength():
		pertotals = perlow + permed + perhigh
		highrange = int(length * 0.667)
		medrange = int(length * 0.334)
		if pertotals <= 1:
			return randrange(1,length,1)
		randpoint = randrange(1,pertotals,1)
		if randpoint >= int(pertotals-perhigh):
			return randrange(highrange,length,1)
		elif randpoint >= int(pertotals - permed) and randpoint < int(pertotals - perhigh):
			return randrange(medrange,highrange,1)
		return randrange(0,medrange,1)
		
			
	def DrawPeak(destx,desty,destz,dirx,diry,dirz):
		if dirx: #set peak drawing starting point
			if dirx == 1:
				start = box.minx
				end = (box.minx + GraduatedLength())+1
				copyblock = level.blockAt(start,desty,destz)
				copyblockdata = level.blockDataAt(start,desty,destz)
			else:
				start = box.maxx - GraduatedLength()
				end = box.maxx-1
				copyblock = level.blockAt(end,desty,destz)
				copyblockdata = level.blockDataAt(end,desty,destz)
			if filterop != "Ignore":
				if filterop == "Do Not Extend" and (copyblock,copyblockdata) in filterblock:
					return
				elif filterop == "Extend Only" and (copyblock,copyblockdata) not in filterblock:
					return
			for blockpos in range(start, end, 1):
				level.setBlockAt(blockpos, desty, destz, copyblock)
				level.setBlockDataAt(blockpos, desty, destz, copyblockdata)
				
			if  (dripblock.ID != 0 or dripclone) and randrange(1,100,1) <= drippypercent:
				if dripspace >= 1:
					if drippynum > 1:
						for dripcount in range(randrange(1,drippynum)):
							drippos = randrange(end,end+dripspace)
							level.setBlockAt(drippos, desty, destz, dripblock.ID if dripblock.ID != 0 else copyblock)
							level.setBlockDataAt(drippos, desty, destz, dripblock.blockData if dripblock.ID != 0 else copyblockdata)
					else:
						if (randrange(1,10)<6):
							drippos = randrange(end,end+dripspace)
							level.setBlockAt(drippos, desty, destz, dripblock.ID if dripblock.ID != 0 else copyblock)
							level.setBlockDataAt(drippos, desty, destz, dripblock.blockData if dripblock.ID != 0 else copyblockdata)

		elif diry:
			if diry == 1:
				start = box.miny
				end = (box.miny + GraduatedLength())+1
				copyblock = level.blockAt(destx,start,destz)
				copyblockdata = level.blockDataAt(destx,start,destz)
			else:
				start = box.maxy - GraduatedLength()
				end = box.maxy-1
				copyblock = level.blockAt(destx,end,destz)
				copyblockdata = level.blockDataAt(destx,end,destz)

			if filterop != "Ignore":
				if filterop == "Do Not Extend" and (copyblock,copyblockdata) in filterblock:
					return
				elif filterop == "Extend Only" and (copyblock,copyblockdata) not in filterblock:
					return

			for blockpos in range(start, end, 1):
				level.setBlockAt(destx, blockpos, destz, copyblock)
				level.setBlockDataAt(destx, blockpos, destz, copyblockdata)
				
			if (dripblock.ID != 0 or dripclone) and randrange(1,100,1) <= drippypercent:
				if dripspace >= 1:
					if drippynum > 1:
						for dripcount in range(randrange(1,drippynum)):
							drippos = randrange(end,end+dripspace)
							level.setBlockAt(destx, drippos, destz, dripblock.ID if dripblock.ID != 0 else copyblock)
							level.setBlockDataAt(destx, drippos, destz, dripblock.blockData if dripblock.ID != 0 else copyblockdata)
					else:
						if (randrange(1,10)<6):
							drippos = randrange(end,end+dripspace)
							level.setBlockAt(destx, drippos, destz, dripblock.ID if dripblock.ID != 0 else copyblock)
							level.setBlockDataAt(destx, drippos, destz, dripblock.blockData if dripblock.ID != 0 else copyblockdata)

		elif dirz:
			if dirz == 1:
				start = box.minz
				end = (box.minz + GraduatedLength())+1
				copyblock = level.blockAt(destx,desty,start)
				copyblockdata = level.blockDataAt(destx,desty,start)
			else:
				start = box.maxz - GraduatedLength()
				end = box.maxz-1
				copyblock = level.blockAt(destx,desty,end)
				copyblockdata = level.blockDataAt(destx,desty,end)

			if filterop != "Ignore":
				if filterop == "Do Not Extend" and (copyblock,copyblockdata) in filterblock:
					return
				elif filterop == "Extend Only" and (copyblock,copyblockdata) not in filterblock:
					return

			for blockpos in range(start, end, 1):
				level.setBlockAt(destx, desty, blockpos, copyblock)
				level.setBlockDataAt(destx, desty, blockpos, copyblockdata)
				
			if  (dripblock.ID != 0 or dripclone) and randrange(1,100,1) <= drippypercent:
				if dripspace >= 1:
					if drippynum > 1:
						for dripcount in range(randrange(1,drippynum)):
							drippos = randrange(end,end+dripspace)
							level.setBlockAt(destx, desty, drippos, dripblock.ID if dripblock.ID != 0 else copyblock)
							level.setBlockDataAt(destx, desty, drippos, dripblock.blockData if dripblock.ID != 0 else copyblockdata)	
					else:
						if (randrange(1,10)<6):
							drippos = randrange(end,end+dripspace)
							level.setBlockAt(destx, desty, drippos, dripblock.ID if dripblock.ID != 0 else copyblock)
							level.setBlockDataAt(destx, desty, drippos, dripblock.blockData if dripblock.ID != 0 else copyblockdata)	
	
	if op == "Draw Compass":
		px = (box.maxx - box.minx) >> 1
		py = (box.maxy - box.miny) >> 1
		pz = (box.maxz - box.minz) >> 1
		px += box.minx
		py += box.miny
		pz += box.minz
		level.setBlockAt(px, py, pz-1, 35)
		level.setBlockDataAt(px, py, pz-1, 14)

		level.setBlockAt(px, py, pz+1, 35)
		level.setBlockDataAt(px, py, pz+1, 0)

		level.setBlockAt(px+1, py, pz, 35)
		level.setBlockDataAt(px+1, py, pz, 15)		

		level.setBlockAt(px-1, py, pz, 35)
		level.setBlockDataAt(px-1, py, pz, 15)
		
	elif op == "Noise":
		if dx:
			numblocks = int((box.maxy-box.miny)*(box.maxz-box.minz))
		elif dy:
			numblocks = int((box.maxx-box.minx)*(box.maxz-box.minz))
		elif dz:
			numblocks = int((box.maxy-box.miny)*(box.maxx-box.minx))

		count = int(numblocks * (percentage*.01))
		itr = 0
		while itr < (count if count <= numblocks else numblocks) and itr < numblocks:
			numtries = 0
			while True:
				x = randrange(box.minx,box.maxx,1)
				y = randrange(box.miny,box.maxy,1)
				z = randrange(box.minz,box.maxz,1)
				if (x,y,z) not in randnumlist:
					randnumlist.append((x,y,z))
					break
				else:
					numtries = numtries + 1
					if numtries > numblocks:
						itr = numblocks
						break
			DrawPeak(x,y,z,dx,dy,dz)
			itr = itr + 1
#	drippynum:
			
#	elif op == "Noise Field":
#		if dx

