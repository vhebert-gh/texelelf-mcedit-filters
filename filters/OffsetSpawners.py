from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Float
from pymclevel import TAG_Double
from pymclevel import TAG_String
from pymclevel import Entity, TileEntity

displayName = "Offset Spawner Spawn Location"

inputs = (
	("Offset X",0.0),
	("Offset Y",0.0),
	("Offset Z",0.0),
	)

def perform(level, box, options):

	ox = options["Offset X"]
	oy = options["Offset Y"]
	oz = options["Offset Z"]
		
	for (chunk, slices, point) in level.getChunkSlices(box):
		for e in chunk.TileEntities:
			x = e["x"].value
			y = e["y"].value
			z = e["z"].value
			if (x,y,z) in box:
				if e["id"].value == "MobSpawner":
					if "SpawnData" in e:
						if "Pos" in e["SpawnData"]:
							e["SpawnData"]["Pos"][0] = TAG_Double(e["SpawnData"]["Pos"][0].value + ox)
							e["SpawnData"]["Pos"][1] = TAG_Double(e["SpawnData"]["Pos"][1].value + oy)
							e["SpawnData"]["Pos"][2] = TAG_Double(e["SpawnData"]["Pos"][2].value + oz)
							chunk.dirty = True

					if "SpawnPotentials" in e:
						for pot in e["SpawnPotentials"]:
							if "Properties" in pot:
								if "Pos" in pot["Properties"]:
									pot["Properties"]["Pos"][0] = TAG_Double(pot["Properties"]["Pos"][0].value + ox)
									pot["Properties"]["Pos"][1] = TAG_Double(pot["Properties"]["Pos"][1].value + oy)
									pot["Properties"]["Pos"][2] = TAG_Double(pot["Properties"]["Pos"][2].value + oz)
									chunk.dirty = True
		for e in chunk.Entities:
			x = e["Pos"][0].value
			y = e["Pos"][1].value
			z = e["Pos"][2].value
			if (x,y,z) in box:
				if e["id"].value == "MinecartSpawner":
					if "SpawnData" in e:
						if "Pos" in e["SpawnData"]:
							e["SpawnData"]["Pos"][0] = TAG_Double(e["SpawnData"]["Pos"][0].value + ox)
							e["SpawnData"]["Pos"][1] = TAG_Double(e["SpawnData"]["Pos"][1].value + oy)
							e["SpawnData"]["Pos"][2] = TAG_Double(e["SpawnData"]["Pos"][2].value + oz)
							chunk.dirty = True

					if "SpawnPotentials" in e:
						for pot in e["SpawnPotentials"]:
							if "Properties" in pot:
								if "Pos" in pot["Properties"]:
									pot["Properties"]["Pos"][0] = TAG_Double(pot["Properties"]["Pos"][0].value + ox)
									pot["Properties"]["Pos"][1] = TAG_Double(pot["Properties"]["Pos"][1].value + oy)
									pot["Properties"]["Pos"][2] = TAG_Double(pot["Properties"]["Pos"][2].value + oz)
									chunk.dirty = True
