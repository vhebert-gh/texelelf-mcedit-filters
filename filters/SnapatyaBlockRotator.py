from pymclevel import TAG_Byte, TAG_Short
from pymclevel import TileEntity

displayName = "MrSnapatya's Block Rotator"

rotations = {	"Downwards (Toward -Y)":0,"Upwards (Toward +Y)":1, "Northwards (Toward -Z)":2,"Southwards (Toward +Z)":3,
				"Westwards (Toward -X)":4,"Eastwards (Toward +X)":5}

inputs = (
	("Set Block Facing Towards:",tuple(rotations.keys())),
	("Operate on:","label"),
	("Chests",False),
	("Trapped Chests",False),
	("Ender Chests",False),
	("Furnaces",False),
	("Active Furnaces",False),
	("Dispensers",False),
	("Droppers",False),
	("Hoppers",False),
	("Pistons",False),
	("Sticky Pistons",False),
	("Pumpkins",False),
	("Jack-o'-Lanterns",False),
	("Repeaters",False),
	("Active Repeaters",False),
	("Comparators",False),
	("Active Comparators",False),
	("Some blocks, such as Furances, technically cannot face upwards or downwards. Specifying either will result in a faceless block.","label"),
	)
	
def perform(level, box, options):
	rot = rotations[options["Set Block Facing Towards:"]]
	entitytypes = []
	if options["Chests"]:
		entitytypes.append(54)
	if options["Trapped Chests"]:
		entitytypes.append(146)
	if options["Ender Chests"]:
		entitytypes.append(130)
	if options["Furnaces"]:
		entitytypes.append(61)
	if options["Active Furnaces"]:
		entitytypes.append(62)
	if options["Dispensers"]:
		entitytypes.append(23)
	if options["Droppers"]:
		entitytypes.append(158)
	if options["Hoppers"]:
		entitytypes.append(154)
	if options["Pistons"]:
		entitytypes.append(33)
	if options["Sticky Pistons"]:
		entitytypes.append(29)
	if options["Pumpkins"]:
		entitytypes.append(86)
	if options["Jack-o'-Lanterns"]:
		entitytypes.append(91)
	if options["Repeaters"]:
		entitytypes.append(93)
	if options["Active Repeaters"]:
		entitytypes.append(94)
	if options["Comparators"]:
		entitytypes.append(149)
	if options["Active Comparators"]:
		entitytypes.append(150)
		
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			for y in xrange(box.miny, box.maxy):
				if level.blockAt(x,y,z) in entitytypes:
					level.setBlockDataAt(x, y, z, rot)