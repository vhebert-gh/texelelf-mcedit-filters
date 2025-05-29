import os
from copy import deepcopy
from pymclevel import mclevel, MCSchematic
from pymclevel.materials import alphaMaterials
from pymclevel import TAG_Compound, TAG_Int, TAG_Int_Array, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List
from pymclevel import BoundingBox
import mcplatform

displayName = "Adventure Multiplex Filter"

inputs = (
	("Operation:",("Export to Schematic","Recalculate Schematic Positions")),
	)
	
def SpawnNormalize(entity, x, y, z):
	if "Pos" in entity:
		entity["Pos"][0] = TAG_Double(entity["Pos"][0].value - x)
		entity["Pos"][1] = TAG_Double(entity["Pos"][1].value - y)
		entity["Pos"][2] = TAG_Double(entity["Pos"][2].value - z)
	if "Leash" in entity:
		if "X" in entity["Leash"] and "Y" in entity["Leash"] and "Z" in entity["Leash"]:
			entity["Leash"]["X"] = TAG_Int(entity["Leash"]["X"].value - x)
			entity["Leash"]["Y"] = TAG_Int(entity["Leash"]["Y"].value - y)
			entity["Leash"]["Z"] = TAG_Int(entity["Leash"]["Z"].value - z)
		
	if "Riding" in entity:
		SpawnNormalize(entity["Riding"], x, y, z)
	if "TileEntityData" in entity:
		SpawnNormalize(entity["TileEntityData"], x, y, z)
	if "SpawnData" in entity:
		SpawnNormalize(entity["SpawnData"], x, y, z)
	if "SpawnPotentials" in entity:
		for e in entity["SpawnPotentials"]:
			if "Properties" in e:
				SpawnNormalize(e["Properties"], x, y, z)
		
def SpawnDenormalize(entity, x, y, z):
	if "Pos" in entity:
		entity["Pos"][0] = TAG_Double(entity["Pos"][0].value + x)
		entity["Pos"][1] = TAG_Double(entity["Pos"][1].value + y)
		entity["Pos"][2] = TAG_Double(entity["Pos"][2].value + z)
	if "Leash" in entity:
		if "X" in entity["Leash"] and "Y" in entity["Leash"] and "Z" in entity["Leash"]:
			entity["Leash"]["X"] = TAG_Int(entity["Leash"]["X"].value + x)
			entity["Leash"]["Y"] = TAG_Int(entity["Leash"]["Y"].value + y)
			entity["Leash"]["Z"] = TAG_Int(entity["Leash"]["Z"].value + z)
	if "Riding" in entity:
		SpawnDenormalize(entity["Riding"], x, y, z)
	if "TileEntityData" in entity:
		SpawnDenormalize(entity["TileEntityData"], x, y, z)
	if "SpawnData" in entity:
		SpawnDenormalize(entity["SpawnData"], x, y, z)
	if "SpawnPotentials" in entity:
		for e in entity["SpawnPotentials"]:
			if "Properties" in e:
				SpawnDenormalize(e["Properties"], x, y, z)

def perform(level, box, options):
	op = options["Operation:"]
	
	if op == "Export to Schematic":
		schematic_file = mcplatform.askSaveFile(mcplatform.lastSchematicsDir or mcplatform.schematicsDir, "Save Schematic As...", "", "Schematic\0*.schematic\0\0", ".schematic")
		if schematic_file == None:
			print "ERROR: No schematic filename provided!"
			return
		if os.path.splitext(schematic_file)[1] != ".schematic":
			print "ERROR: You must specify a .schematic file!"
			return

		tileposlist = []
		for (chunk, _, _) in level.getChunkSlices(box):
			tileposlist = tileposlist + chunk.getTileEntitiesInBox(box)

		entposlist = []
		for (chunk, _, _) in level.getChunkSlices(box):
			entposlist = entposlist + chunk.getEntitiesInBox(box)

		schematic = level.extractSchematic(box)

		del schematic.root_tag["TileEntities"]
		schematic.root_tag["TileEntities"] = TAG_List()
		for tileent in tileposlist:
			schematic.TileEntities.append(deepcopy(tileent))

		del schematic.root_tag["Entities"]
		schematic.root_tag["Entities"] = TAG_List()
		for ent in entposlist:
			schematic.Entities.append(deepcopy(ent))

		for tileent in schematic.TileEntities:
			x = tileent["x"].value
			y = tileent["y"].value
			z = tileent["z"].value
			tileent["x"] = TAG_Int(x - box.minx)
			tileent["y"] = TAG_Int(y - box.miny)
			tileent["z"] = TAG_Int(z - box.minz)
			if tileent["id"].value == "MobSpawner":
				SpawnNormalize(tileent, x, y, z)

		for ent in schematic.Entities:
			x = ent["Pos"][0].value
			y = ent["Pos"][1].value
			z = ent["Pos"][2].value
			ent["Pos"][0] = TAG_Double(x - box.minx)
			ent["Pos"][1] = TAG_Double(y - box.miny)
			ent["Pos"][2] = TAG_Double(z - box.minz)
			if ent["id"].value == "MinecartSpawner":
				if "SpawnData" in ent:
					SpawnNormalize(ent["SpawnData"], x, y, z)
				if "SpawnPotentials" in ent:
					for e in ent["SpawnPotentials"]:
						if "Properties" in e:
							SpawnNormalize(e["Properties"], x, y, z)
			elif ent["id"].value in ("Painting","ItemFrame"):
				ent["TileX"] = TAG_Int(ent["TileX"].value - box.minx)
				ent["TileY"] = TAG_Int(ent["TileY"].value - box.miny)
				ent["TileZ"] = TAG_Int(ent["TileZ"].value - box.minz)
			if "Riding" in ent:
				SpawnNormalize(ent["Riding"], x, y, z)

		schematic.saveToFile(schematic_file)

	elif op == "Recalculate Schematic Positions":
		for (chunk, _, _) in level.getChunkSlices(box):
			for tileent in chunk.TileEntities:
				if tileent["id"].value == "MobSpawner":
					x = tileent["x"].value
					y = tileent["y"].value
					z = tileent["z"].value
					if (x,y,z) in box:
						SpawnDenormalize(tileent, x, y, z)
						chunk.dirty = True
			for ent in chunk.Entities:
				x = ent["Pos"][0].value
				y = ent["Pos"][1].value
				z = ent["Pos"][2].value
				if (x,y,z) in box:
					if ent["id"].value == "MinecartSpawner":
						if "SpawnData" in ent:
							SpawnDenormalize(ent["SpawnData"], x, y, z)
						if "SpawnPotentials" in ent:
							for e in ent["SpawnPotentials"]:
								if "Properties" in e:
									SpawnDenormalize(e["Properties"], x, y, z)
					if "Riding" in ent:
						SpawnDenormalize(ent["Riding"], x, y, z)
					chunk.dirty = True
