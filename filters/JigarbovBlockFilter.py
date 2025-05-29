from random import randint, shuffle
from pymclevel.materials import alphaMaterials

displayName = "Jigarbov's Block Filter"

class FakeBlock:
	ID = 0
	blockData = 0
	def __init__(self, ID, Data):
		self.ID = ID
		self.blockData = Data

inputs = [
	(("Filter Operation:", ("Fill (Ignore Target Blocks)","Replace Only Target Blocks","Do Not Replace Target Blocks")),
	("Ignore Block Data", False),
	("If you wish to use Air blocks as a source or a target block, ensure that Source Block 1 and/or Target Block 1 is set to air; \"Air\" is otherwise ignored for the rest of the Block options.\n","label"),
	("The two text boxes below are used to provide comma-separated lists of more source and target blocks in addition to those specified on the Target and Source tabs.\n"
		"For Source Blocks, the notation is as follows: \"ID:Data:Weight\", e.g.:\n\t1:0:60,137:0:1,210:5:20\n"
		"For Target Blocks, the notation is as follows: \"ID:Data\", e.g.:\n\t1:0,137:0,4:4","label"),
	("Extra Source Blocks:",("string","value=None","width=400")),
	("Extra Target Blocks:",("string","value=None","width=400")),
	("General Settings","title"),),
	
	(("Source Block 1", alphaMaterials.Air),
	("Source Block 1 Weight", 0),
	("Source Block 2", alphaMaterials.Air),
	("Source Block 2 Weight", 0),
	("Source Block 3", alphaMaterials.Air),
	("Source Block 3 Weight", 0),
	("Source Block 4", alphaMaterials.Air),
	("Source Block 4 Weight", 0),
	("Source Block 5", alphaMaterials.Air),
	("Source Block 5 Weight", 0),
	("Source Block 6", alphaMaterials.Air),
	("Source Block 6 Weight", 0),
	("Source Block 7", alphaMaterials.Air),
	("Source Block 7 Weight", 0),
	("Source Block 8", alphaMaterials.Air),
	("Source Block 8 Weight", 0),
	("Source Blocks","title")),
	
	(("Target Block 1", alphaMaterials.Air),
	("Target Block 2", alphaMaterials.Air),
	("Target Block 3", alphaMaterials.Air),
	("Target Block 4", alphaMaterials.Air),
	("Target Block 5", alphaMaterials.Air),
	("Target Block 6", alphaMaterials.Air),
	("Target Block 7", alphaMaterials.Air),
	("Target Block 8", alphaMaterials.Air),
	("Target Block 9", alphaMaterials.Air),
	("Target Block 10", alphaMaterials.Air),
	("Target Blocks","title")),
	
	]

def perform(level, box, options):
	ReplaceBlock = []
	FilterBlock = []
	PercentList = []

	if options["Source Block 1 Weight"] > 0:
		ReplaceBlock.append(options["Source Block 1"])
		for c in xrange(options["Source Block 1 Weight"]):
			PercentList.append(options["Source Block 1"])
	if options["Source Block 2"].ID != 0:
		ReplaceBlock.append(options["Source Block 2"])
		for c in xrange(options["Source Block 2 Weight"]):
			PercentList.append(options["Source Block 2"])
	if options["Source Block 3"].ID != 0:
		ReplaceBlock.append(options["Source Block 3"])
		for c in xrange(options["Source Block 3 Weight"]):
			PercentList.append(options["Source Block 3"])
	if options["Source Block 4"].ID != 0:
		ReplaceBlock.append(options["Source Block 4"])
		for c in xrange(options["Source Block 4 Weight"]):
			PercentList.append(options["Source Block 4"])
	if options["Source Block 5"].ID != 0:
		FilterBlock.append(options["Source Block 5"])
		for c in xrange(options["Source Block 5 Weight"]):
			PercentList.append(options["Source Block 5"])
	if options["Source Block 6"].ID != 0:
		FilterBlock.append(options["Source Block 6"])
		for c in xrange(options["Source Block 6 Weight"]):
			PercentList.append(options["Source Block 6"])
	if options["Source Block 7"].ID != 0:
		FilterBlock.append(options["Source Block 7"])
		for c in xrange(options["Source Block 7 Weight"]):
			PercentList.append(options["Source Block 7"])
	if options["Source Block 8"].ID != 0:
		FilterBlock.append(options["Source Block 8"])
		for c in xrange(options["Source Block 8 Weight"]):
			PercentList.append(options["Source Block 8"])

	op = options["Filter Operation:"]
	if op == "Fill (Ignore Target Blocks)":
		op = 0
	elif op == "Replace Only Target Blocks":
		op = 1
	elif op == "Do Not Replace Target Blocks":
		op = 2
	ignore = options["Ignore Block Data"]
		
	FilterBlock.append((options["Target Block 1"].ID,(options["Target Block 1"].blockData if not ignore else 0)))
	if options["Target Block 2"].ID != 0:
		FilterBlock.append((options["Target Block 2"].ID,(options["Target Block 2"].blockData if not ignore else 0)))
	if options["Target Block 3"].ID != 0:
		FilterBlock.append((options["Target Block 3"].ID,(options["Target Block 3"].blockData if not ignore else 0)))
	if options["Target Block 4"].ID != 0:
		FilterBlock.append((options["Target Block 4"].ID,(options["Target Block 4"].blockData if not ignore else 0)))
	if options["Target Block 5"].ID != 0:
		FilterBlock.append((options["Target Block 5"].ID,(options["Target Block 5"].blockData if not ignore else 0)))
	if options["Target Block 6"].ID != 0:
		FilterBlock.append((options["Target Block 6"].ID,(options["Target Block 6"].blockData if not ignore else 0)))
	if options["Target Block 7"].ID != 0:
		FilterBlock.append((options["Target Block 7"].ID,(options["Target Block 7"].blockData if not ignore else 0)))
	if options["Target Block 8"].ID != 0:
		FilterBlock.append((options["Target Block 8"].ID,(options["Target Block 8"].blockData if not ignore else 0)))
	if options["Target Block 9"].ID != 0:
		FilterBlock.append((options["Target Block 9"].ID,(options["Target Block 9"].blockData if not ignore else 0)))
	if options["Target Block 10"].ID != 0:
		FilterBlock.append((options["Target Block 10"].ID,(options["Target Block 10"].blockData if not ignore else 0)))

	exsource = options["Extra Source Blocks:"]
	if exsource.upper() != "NONE":
		for src in exsource.split(","):
			try:
				ID, Data, Weight = src.split(":")
			except:
				raise Exception("ERROR: Incorrectly formatted Source Block field!")
			ID = int(ID)
			Data = int(Data) if not ignore else 0
			for c in xrange(int(Weight)):
				PercentList.append(FakeBlock(ID,Data))

	extarget = options["Extra Target Blocks:"]
	if extarget.upper() != "NONE":
		for tgt in extarget.split(","):
			try:
				ID, Data = tgt.split(":")
			except:
				raise Exception("ERROR: Incorrectly formatted Target Block field!")
			ID = int(ID)
			Data = int(Data) if not ignore else 0
			FilterBlock.append((ID,Data))

	shuffle(PercentList)
	if not PercentList:
		raise Exception("ERROR: No source blocks have been specified for this operation!")
	
	for (chunk, slices, garbage) in level.getChunkSlices(box):
		for x in xrange(slices[0].start, slices[0].stop):
			for z in xrange(slices[1].start, slices[1].stop):
				for y in xrange(slices[2].start, slices[2].stop):
					rng = randint(0,len(PercentList)-1)
					if op == 0:
						block = PercentList[rng]
						chunk.Blocks[x, z, y] = block.ID
						chunk.Data[x, z, y] = block.blockData
						chunk.dirty = True
					elif (op == 1) and ((chunk.Blocks[x, z, y],(chunk.Data[x, z, y] if not ignore else 0)) in FilterBlock):
						block = PercentList[rng]
						chunk.Blocks[x, z, y] = block.ID
						chunk.Data[x, z, y] = block.blockData
						chunk.dirty = True
					elif (op == 2) and ((chunk.Blocks[x, z, y],(chunk.Data[x, z, y] if not ignore else 0)) not in FilterBlock):
						block = PercentList[rng]
						chunk.Blocks[x, z, y] = block.ID
						chunk.Data[x, z, y] = block.blockData
						chunk.dirty = True
						
