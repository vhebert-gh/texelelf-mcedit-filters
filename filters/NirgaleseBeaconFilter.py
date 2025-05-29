from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String
from pymclevel import TileEntity

displayName = "Nirgalese Beacon Filter"

Effects = {
	"Speed": 1,
	"Slowness": 2,
	"Haste": 3,
	"Mining Fatigue": 4,
	"Strength": 5,
	"Instant Health": 6,
	"Instant Damage": 7,
	"Jump Boost": 8,
	"Nausea": 9,
	"Regeneration": 10,
	"Resistance": 11,
	"Fire Resistance": 12,
	"Water Breathing": 13,
	"Invisibility": 14,
	"Blindness": 15,
	"Night Vision": 16,
	"Hunger": 17,
	"Weakness": 18,
	"Poison": 19,
	"Wither": 20,
	}
	
EffectKeys = ()
for key in Effects.keys():
	EffectKeys = EffectKeys + (key,)
	
inputs = (
	("Operation:", ("Modify","Fill")),
	("Primary Effect", EffectKeys),
	("Secondary Effect", EffectKeys),
	("Number of Levels on Beacon",0),
	)

def perform(level, box, options):

	op = options["Operation:"]
	
	primary = options["Primary Effect"]
	primary = Effects[primary]
	secondary = options["Secondary Effect"]
	secondary = Effects[secondary]
	levels = options["Number of Levels on Beacon"]
	
	for (chunk, slices, point) in level.getChunkSlices(box):
		if op == "Modify":
			for e in chunk.TileEntities:
				x = e["x"].value
				y = e["y"].value
				z = e["z"].value
				if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
					if e["id"].value == "Beacon":
						e["Primary"] = TAG_Int(primary)
						e["Secondary"] = TAG_Int(secondary)
						if levels > 0:
							e["Levels"] = TAG_Int(levels)
						chunk.dirty = True
		else:
			(cx,cz) = chunk.chunkPosition
			cposx = cx * 16
			cposz = cz * 16
			for y in range(box.miny,box.maxy,1):
				for x in range((cposx if (cposx > box.minx) else box.minx),(cposx+16 if ((cposx+16) < box.maxx) else box.maxx),1):
					for z in range((cposz if (cposz > box.minz) else box.minz),(cposz+16 if((cposz+16) < box.maxz) else box.maxz),1):
						level.setBlockAt(x, y, z, 138)
						e = TileEntity.Create("Beacon")
						e["Primary"] = TAG_Int(primary)
						e["Secondary"] = TAG_Int(secondary)
						if levels > 0:
							e["Levels"] = TAG_Int(levels)
						TileEntity.setpos(e, (x, y, z))
						chunk.TileEntities.append(e)
			chunk.dirty = True
