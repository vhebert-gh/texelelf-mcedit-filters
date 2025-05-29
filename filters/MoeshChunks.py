from pymclevel import TAG_String, TAG_Byte, TAG_Compound, TAG_Int
from pymclevel import MCSchematic
import inspect

displayName = "Moesh's Chunk Loader Filter"

mobs = ("Bat","Blaze","CaveSpider","Chicken","Cow","Creeper","EnderDragon",
		"Enderman","Ghast","Giant","Guardian","LavaSlime","MushroomCow","Ozelot","Pig","PigZombie","Rabbit",
		"Sheep","Silverfish","Skeleton","Slime","SnowMan","Spider","Squid",
		"Villager","VillagerGolem","Witch","WitherBoss","Wolf","Zombie")

entity_list =	("Arrow","Snowball","Fireball","SmallFireball","WitherSkull","FireworksRocketEntity","ThrownEnderpearl",
				"ThrownPotion","ThrownExpBottle","Item","XPOrb","EyeOfEnderSignal","EnderCrystal",
				"MinecartChest","MinecartFurnace","MinecartHopper","MinecartRideable","MinecartTNT","Boat","PrimedTnt","FallingSand")

inputs = (
	("Chunk loading entity:",mobs+entity_list),
	("Spawn coordinates (X Y Z):",("string","value=0 0 0")),
	("Entity team name:",("string","value=TheMounties")),
	("Entity base name:",("string","value=moeshroom")),
	)

def CommandBlock(x,y,z,command):
	cmd = TAG_Compound()
	cmd["x"] = TAG_Int(x)
	cmd["y"] = TAG_Int(y)
	cmd["z"] = TAG_Int(z)
	cmd["id"] = TAG_String("Control")
	cmd["Command"] = TAG_String(command)
	cmd["TrackOutput"] = TAG_Byte(0)
	return cmd

def perform(level, box, options):
	editor = inspect.stack()[1][0].f_locals.get('self', None).editor

	entitytype = options["Chunk loading entity:"]
	centralcoords = options["Spawn coordinates (X Y Z):"]
	team = options["Entity team name:"]
	name = options["Entity base name:"]

	baseselector = "@e[type="+entitytype+",name="+name+"%d]"
	coords = centralcoords.split(" ")
	basecoords = "x="+coords[0]+",y="+coords[1]+",z="+coords[2]+",r=1]"

	basesummon = "summon "+entitytype+" "+centralcoords+" "
	
	chunklist = [chunks for chunks, _, _ in level.getChunkSlices(box)]
	schmwidth = len(chunklist)
	schematic = MCSchematic((schmwidth+1, 1, 3), mats=level.materials)

	x = 0
	for c in chunklist:
		summon = basesummon
		selector = baseselector % x
		if entitytype in ("Fireball","SmallFireball","WitherSkull"):
			summon += "{CustomName:"+name+"%d,direction:[0d,0d,0d]}" % x
		elif entitytype in mobs:
			summon += "{CustomName:"+name+"%d,Silent:1b,Invulnerable:1b,ActiveEffects:[{Id:14b,Duration:2147483647,ShowParticles:0b}],Attributes:[{Name:\"generic.followRange\",Base:0d},{Name:\"generic.movementSpeed\",Base:0d}]}" % x
		else:
			summon += ""
		cx, cz = c.chunkPosition
		cx <<= 4
		cz <<= 4
		cx += 8
		cz += 8
		schematic.TileEntities.append(CommandBlock(x,0,0,summon))
		schematic.setBlockAt(x,0,0,137)
		schematic.TileEntities.append(CommandBlock(x,0,2,"spreadplayers "+str(cx)+" "+str(cz)+" 0 1 false "+selector))
		schematic.setBlockAt(x,0,2,137)
		x += 1
	else:
		schematic.TileEntities.append(CommandBlock(x,0,0,"scoreboard teams join "+team+" @e[type="+entitytype+","+basecoords))
		schematic.setBlockAt(x,0,0,137)
		# schematic.TileEntities.append(CommandBlock(x,0,2,"tp @e[team="+team+"] "+centralcoords,True))
		# schematic.setBlockAt(x,0,2,137)

	editor.addCopiedSchematic(schematic)
	raise Exception("Schematic successfully added to clipboard.")
