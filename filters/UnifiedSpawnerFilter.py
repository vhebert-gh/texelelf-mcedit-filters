import os
import fnmatch
import math
import uuid
from numpy import zeros, fromiter, append
from copy import deepcopy
from random import randrange
from pymclevel import mclevel
from pymclevel import MCSchematic
from pymclevel.materials import alphaMaterials
from pymclevel import TAG_Compound, TAG_Int, TAG_Int_Array, TAG_Short, TAG_Byte, TAG_String, TAG_Float, TAG_Double, TAG_List, TAG_Long
from pymclevel import TileEntity, Entity
import mcplatform

displayName = "Unified Spawner Filter"

sectional = "\xA7"

entity_list = (	"None","Arrow","Snowball","Fireball","SmallFireball","WitherSkull","FireworksRocketEntity","ThrownEnderpearl",
				"ThrownPotion","ThrownExpBottle","Item","XPOrb","EyeOfEnderSignal","EnderCrystal",
				"MinecartChest","MinecartFurnace","MinecartHopper","MinecartRideable","MinecartTNT","Boat","PrimedTnt","FallingSand")
				
monsters = ("None","Bat","Blaze","CaveSpider","Chicken","Cow","Creeper","EnderDragon",
			"Enderman","EntityHorse","Ghast","Giant","Guardian","LavaSlime","MushroomCow","Ozelot","Pig","PigZombie","Rabbit",
			"Silverfish","Sheep","Skeleton","Slime","SnowMan","Spider","Squid",
			"Villager","VillagerGolem","Witch","WitherBoss","Wolf","Zombie",)

Professions = {"Farmer (brown)": 0,"Librarian (white)": 1,"Priest (purple)": 2,"Blacksmith (black apron)": 3,"Butcher (white apron)": 4,"Villager (green)": 5}
	
ProfessionKeys = ("N/A",)
for key in Professions.keys():
	ProfessionKeys = ProfessionKeys + (key,)
	
HorseTypes = { "Horse":0, "Donkey":1, "Mule":2, "Zombie":3, "Skeleton":4}

WoolColors={"White": 0,"Orange": 1,"Magenta": 2,"Light Blue": 3,"Yellow": 4,"Lime": 5,"Pink": 6,"Gray": 7,"Light Gray": 8,
			"Cyan": 9,"Purple": 10,"Blue": 11,"Brown": 12,"Green": 13,"Red": 14,"Black": 15,"Random": 16}

Wools=("White","Orange","Magenta","Light Blue","Yellow","Lime","Pink","Gray","Light Gray","Cyan","Purple","Blue","Brown","Green","Red","Black","Random")

enchantments = ("None","Protection","Fire Protection","Feather Falling","Blast Protection","Projectile Protection","Respiration",
				"Aqua Affinity","Thorns","Sharpness","Smite","Bane of Arthropods","Knockback","Fire Aspect","Looting","Efficiency","Silk Touch",
				"Unbreaking","Fortune","Power","Punch","Flame","Infinity")
	
enchantment_vals = {"None":-1,"Protection":0,"Fire Protection":1,"Feather Falling":2,"Blast Protection":3,"Projectile Protection":4,
					"Respiration":5,"Aqua Affinity":6,"Thorns":7,"Sharpness":16,"Smite":17,"Bane of Arthropods":18,"Knockback":19,"Fire Aspect":20,
					"Looting":21,"Efficiency":32,"Silk Touch":33,"Unbreaking":34,"Fortune":35,"Power":48,"Punch":49,"Flame":50,"Infinity":51}
	
splash_potions = (	"None (Water bottle)","Fire Resist (2:15)","Fire Resist (6:00)","Instant Health","Instant Health II","Instant Damage","Instant Damage II",
					"Invisibility (2:15)", "Invisibility (6:00)", "Night Vision (2:15)","Night Vision (6:00)","Poison (0:33)","Poison (1:30)","Poison II (0:16)","Poison II (0:45)",
					"Regeneration (0:33)","Regeneration (1:30)","Regeneration II (0:16)","Regeneration II (0:45)","Slowness (1:07)","Slowness (3:00)","Speed (2:15)","Speed (6:00)",
					"Speed II (1:07)","Speed II (3:00)","Strength (2:15)","Strength (6:00)","Strength II (1:07)","Strength II (3:00)","Weakness (1:07)","Weakness (3:00)")

potion_list = {		"None (Water bottle)":0,"Strength II (3:00)": 32761,"Poison II (0:45)": 32756,"Speed II (3:00)": 32754,"Regeneration II (0:45)": 32753,
					"Slowness (3:00)": 32762,"Strength (6:00)": 32729,"Weakness (3:00)": 32760,"Poison (1:30)": 32724,"Fire Resist (6:00)": 32755,
					"Speed (6:00)": 32722,"Regeneration (1:30)": 32721,"Strength II (1:07)": 32697,"Poison II (0:16)": 32692,"Speed II (1:07)": 32690,
					"Regeneration II (0:16)": 32689,"Slowness (1:07)": 32698,"Strength (2:15)": 32665,"Weakness (1:07)": 32696,"Poison (0:33)": 32660,
					"Fire Resist (2:15)": 32691,"Speed (2:15)": 32658,"Regeneration (0:33)": 32657,"Instant Health": 32725,"Instant Health II": 32757,
					"Instant Damage": 32732,"Instant Damage II": 32764, "Invisibility (2:15)":32702, "Invisibility (6:00)":32766, "Night Vision (2:15)":32694,
					"Night Vision (6:00)":32758}
				
potion_effects_vals = {	"None": -1,"Speed": 1,"Slowness": 2,"Haste": 3,"Mining Fatigue": 4,"Strength": 5,"Instant Health": 6,"Instant Damage": 7,
						"Jump Boost": 8,"Nausea": 9,"Regeneration": 10,"Resistance": 11,"Fire Resistance": 12,"Water Breathing": 13,"Invisibility": 14,
						"Blindness": 15,"Night Vision": 16,"Hunger": 17,"Weakness": 18,"Poison": 19,"Wither": 20,"Health Boost":21,"Absorption":22,"Saturation":23}
	
potion_effects = (	"None","Speed","Slowness","Haste","Mining Fatigue","Strength","Instant Health",
					"Instant Damage","Jump Boost","Nausea","Regeneration","Resistance","Fire Resistance",
					"Water Breathing","Invisibility","Blindness","Night Vision","Hunger","Weakness",
					"Poison","Wither","Health Boost","Absorption","Saturation")

fireworks =			("Small Ball","Large Ball","Star-Shaped","Creeper-Shaped","Burst")
fireworks_vals =	{"Small Ball":0,"Large Ball":1,"Star-Shaped":2,"Creeper-Shaped":3,"Burst":4}

HeadVals = {"Skeleton":0,"Wither Skeleton":1,"Zombie":2,"Steve or Player":3,"Creeper":4}
rotvals = {	"South": 0x8,"South-Southwest": 0x9,"Southwest": 0xA,"West-Southwest":0xB,
			"West":0xC,"West-Northwest":0xD,"Northwest":0xE,"North-Northwest":0xF,
			"North":0x0,"North-Northeast":0x1,"Northeast":0x2,"East-Northeast":0x3,
			"East":0x4,"East-Southeast":0x5,"Southeast":0x6,"South-Southeast":0x7}

block_map = {
	0:"minecraft:air",1:"minecraft:stone",2:"minecraft:grass",3:"minecraft:dirt",4:"minecraft:cobblestone",5:"minecraft:planks",6:"minecraft:sapling",
	7:"minecraft:bedrock",8:"minecraft:flowing_water",9:"minecraft:water",10:"minecraft:flowing_lava",11:"minecraft:lava",12:"minecraft:sand",13:"minecraft:gravel",
	14:"minecraft:gold_ore",15:"minecraft:iron_ore",16:"minecraft:coal_ore",17:"minecraft:log",18:"minecraft:leaves",19:"minecraft:sponge",20:"minecraft:glass",
	21:"minecraft:lapis_ore",22:"minecraft:lapis_block",23:"minecraft:dispenser",24:"minecraft:sandstone",25:"minecraft:noteblock",26:"minecraft:bed",
	27:"minecraft:golden_rail",28:"minecraft:detector_rail",29:"minecraft:sticky_piston",30:"minecraft:web",31:"minecraft:tallgrass",32:"minecraft:deadbush",
	33:"minecraft:piston",34:"minecraft:piston_head",35:"minecraft:wool",36:"minecraft:piston_extension",37:"minecraft:yellow_flower",38:"minecraft:red_flower",
	39:"minecraft:brown_mushroom",40:"minecraft:red_mushroom",41:"minecraft:gold_block",42:"minecraft:iron_block",43:"minecraft:double_stone_slab",
	44:"minecraft:stone_slab",45:"minecraft:brick_block",46:"minecraft:tnt",47:"minecraft:bookshelf",48:"minecraft:mossy_cobblestone",49:"minecraft:obsidian",
	50:"minecraft:torch",51:"minecraft:fire",52:"minecraft:mob_spawner",53:"minecraft:oak_stairs",54:"minecraft:chest",55:"minecraft:redstone_wire",
	56:"minecraft:diamond_ore",57:"minecraft:diamond_block",58:"minecraft:crafting_table",59:"minecraft:wheat",60:"minecraft:farmland",61:"minecraft:furnace",
	62:"minecraft:lit_furnace",63:"minecraft:standing_sign",64:"minecraft:wooden_door",65:"minecraft:ladder",66:"minecraft:rail",67:"minecraft:stone_stairs",
	68:"minecraft:wall_sign",69:"minecraft:lever",70:"minecraft:stone_pressure_plate",71:"minecraft:iron_door",72:"minecraft:wooden_pressure_plate",
	73:"minecraft:redstone_ore",74:"minecraft:lit_redstone_ore",75:"minecraft:unlit_redstone_torch",76:"minecraft:redstone_torch",77:"minecraft:stone_button",
	78:"minecraft:snow_layer",79:"minecraft:ice",80:"minecraft:snow",81:"minecraft:cactus",82:"minecraft:clay",83:"minecraft:reeds",84:"minecraft:jukebox",
	85:"minecraft:fence",86:"minecraft:pumpkin",87:"minecraft:netherrack",88:"minecraft:soul_sand",89:"minecraft:glowstone",90:"minecraft:portal",
	91:"minecraft:lit_pumpkin",92:"minecraft:cake",93:"minecraft:unpowered_repeater",94:"minecraft:powered_repeater",
	95:"minecraft:stained_glass",96:"minecraft:trapdoor",97:"minecraft:monster_egg",98:"minecraft:stonebrick",
	99:"minecraft:brown_mushroom_block",100:"minecraft:red_mushroom_block",101:"minecraft:iron_bars",102:"minecraft:glass_pane",103:"minecraft:melon_block",
	104:"minecraft:pumpkin_stem",105:"minecraft:melon_stem",106:"minecraft:vine",107:"minecraft:fence_gate",108:"minecraft:brick_stairs",109:"minecraft:stone_brick_stairs",
	110:"minecraft:mycelium",111:"minecraft:waterlily",112:"minecraft:nether_brick",113:"minecraft:nether_brick_fence",114:"minecraft:nether_brick_stairs",
	115:"minecraft:nether_wart",116:"minecraft:enchanting_table",117:"minecraft:brewing_stand",118:"minecraft:cauldron",119:"minecraft:end_portal",
	120:"minecraft:end_portal_frame",121:"minecraft:end_stone",122:"minecraft:dragon_egg",123:"minecraft:redstone_lamp",124:"minecraft:lit_redstone_lamp",
	125:"minecraft:double_wooden_slab",126:"minecraft:wooden_slab",127:"minecraft:cocoa",128:"minecraft:sandstone_stairs",129:"minecraft:emerald_ore",
	130:"minecraft:ender_chest",131:"minecraft:tripwire_hook",132:"minecraft:tripwire",133:"minecraft:emerald_block",134:"minecraft:spruce_stairs",
	135:"minecraft:birch_stairs",136:"minecraft:jungle_stairs",137:"minecraft:command_block",138:"minecraft:beacon",139:"minecraft:cobblestone_wall",
	140:"minecraft:flower_pot",141:"minecraft:carrots",142:"minecraft:potatoes",143:"minecraft:wooden_button",144:"minecraft:skull",145:"minecraft:anvil",
	146:"minecraft:trapped_chest",147:"minecraft:light_weighted_pressure_plate",148:"minecraft:heavy_weighted_pressure_plate",149:"minecraft:unpowered_comparator",
	150:"minecraft:powered_comparator",151:"minecraft:daylight_detector",152:"minecraft:redstone_block",153:"minecraft:quartz_ore",154:"minecraft:hopper",
	155:"minecraft:quartz_block",156:"minecraft:quartz_stairs",157:"minecraft:activator_rail",158:"minecraft:dropper",159:"minecraft:stained_hardened_clay",
	160:"minecraft:stained_glass_pane",161:"minecraft:leaves2",162:"minecraft:log2",163:"minecraft:acacia_stairs",164:"minecraft:dark_oak_stairs",165:"minecraft:slime",166:"minecraft:barrier",
	167:"minecraft:iron_trapdoor",168:"minecraft:prismarine",169:"minecraft:sea_lantern",
	170:"minecraft:hay_block",171:"minecraft:carpet",172:"minecraft:hardened_clay",173:"minecraft:coal_block",174:"minecraft:packed_ice",175:"minecraft:double_plant"
}

inputs = [
	(("Operation:",("Fill",
					"Random Fill Number",
					"Random Fill Percent",
					"Grid Fill",
					"Entity -> Spawner",
					"TileEntity -> FallingSand Spawner",
					"Spawner -> Falling Spawner",
					"Spawner -> Spawner Minecart",
					"Spawner Minecart -> Spawner",
					"Stack SpawnPotentials Slots into Riding Entities",
					"Unstack Riding Entities into SpawnPotentials Slots",
					"Prefix to SpawnPotentials Slot List",
					"Append to SpawnPotentials Slot List",
					"Bring SpawnPotentials Slot to Front",
					"Set SpawnPotentials Slot Weight",
					"List SpawnPotentials Slots in Console",
					"Set SpawnPotentials Slot as Active Spawn",
					"Clear SpawnPotentials Slot",
					"Add New Properties for \"Entity\\Mob Type\"",
					"Clear All Properties",
					"Set Only Position", 
					"Set Only Velocity", 
					"Set Only Spawn Conditions", 
					"Add Potion Effect",
					"Clear Potion Effects", 
					"Add Enchant",
					"Clear Enchants",
					"Add or Edit Attribute (Mobs Only)",
					"Add or Edit Attribute Modifier (Mobs and Items)",
					"List Attributes in Console",
					"Clear Attributes (Mobs Only)",
					"Clear Attribute Modifiers (Item Entities Only)",
					"Set Mob Name Properties",
					"Set Name",
					"Clear Name",
					"Add Lore",
					"Clear Lores",
					"Modify Fireworks",
					"Output SpawnPotentials Slot Properties to Console",
					"Output Spawner Properties to Console")),
	("Number or Percentage/Grid Size",10.0),
	("Use Schematic:",False),
	("Spawner Type:",("Mob Spawner Block","Mob Spawner Minecart")),
	("Mob Type",monsters),
	("Entity Type",entity_list),
	("SpawnPotentials Slot",(1,1,128)),
	("Slot Weight",(1,-2147483648,2147483647)),
	("Block Replace Mode", ("None","Replace","Do Not Replace")),
	("Block to (Not) Replace", alphaMaterials.Air),
	("Ticks Until Spawn", (20,-32768,32767)),
	("Min Ticks Between Spawns",(200,0,32767)),
	("Max Ticks Between Spawns",(800,1,32767)),
	("Max Number of Entities Per Spawn", (4,0,32767)),
	("Maximum Spawned Entities in Area",(6,0,32767)),
	("Spawning Range",(4,0,32767)),
	("Player Detection Radius", (16,0,32767)),
	("Spawner", "title"),),

	(("Positioning Mode",("Ignore Values","Relative","Absolute")),
	("Auto-center X and Z to middle of block",True),
	("PosX",0.0),
	("PosY",0.0),
	("PosZ",0.0),
	("Lock SpawnData tag",False),
	(" ","label"),
	(" ","label"),
	(" ","label"),
	(" ","label"),
	(" ","label"),
	("Use Velocity Settings", False),
	("VelocityX", 0.0),
	("VelocityY", 0.0),
	("VelocityZ", 0.0),
	("Fire", (-1,-32768,32767)),
	("FallDistance", 0.0),
	("Invulnerable",False),
	("Common","title"),),

	
	(("Mob Name",("string","value=None")),
	("Mob Name is visible",False),
	("Persistent (Won't Despawn)",False),
	("Can Pick Up Loot",False),
	("Use Mob's Default Health Value",True),
	("Health", 0.0),
	("Absorption Health Amount",4.0),
	("Air", (300,-32768,32767)),
	("AttackTime", (0,-32768,32767)),
	("HurtTime", (0,-32768,32767)),
	("Enderman is Carrying...", alphaMaterials.Air),
	("Villager Profession", ProfessionKeys),
	("Slime Size", (0,-128,127)),
	("Love Mode Ticks", (0,-2147483648,2147483647)),
	("Child/Adult Age", (0,-2147483648,2147483647)),
	("Zombie Pig Aggro Level",(0,-32768,32767)),
	("Wither Skeleton", False),
	("Zombie Villager",False),
	("Baby Zombie",False),
	("Mob 1","title"),),
	
	(("Powered Creeper", False),
	("Creeper Explosion Radius",(3,-128,127)),
	("Creeper Fuse Length (ticks)",(30,-32768,32767)),
	("Ghast Fireball Explosion Power",(1,-2147483648,2147483647)),
	("Elder Guardian",False),
	("Angry Wolf", False),
	("Saddled Pig", False),
	("Shorn Sheep", False),
	("Sheep Wool Color", Wools),
	("\n\n","label"),
	("Rabbit Type (99 for killer rabbit)",(0,-2147483648,2147483647)),
	("Horse Type:", ("Horse", "Donkey", "Mule", "Zombie", "Skeleton")),
	("Horse has Chest",False),
	("Horse is Tame",False),
	("Horse's Temper",(0,-2147483648,2147483647)),
	("Horse Variant:",(0,-2147483648,2147483647)),
	("Horse Saddle Item ID:",(0,-32768,32767)),
	("Horse Armor Item ID:",(0,-32768,32767)),
	("Mob 2","title"),),

	(("Modify Fireworks Operation:",("Add Fireworks Ball to Rocket","Add Burst Color to Ball","Add Fade Color to Ball",
				"List all Fireworks Balls in Rocket","Set Rocket Flight and Max Rocket Flight Duration","Clear Fireworks Ball from Rocket",)),
	("Current Rocket Flight Duration (ticks)", (1,-2147483648,2147483647)),
	("Max Flight Duration Until Explosion (ticks)", (28,-2147483648,2147483647)),
	("Shape:",fireworks),
	("Ball Slot",(1,1,1000)),
	("Burst Color",("string","value=#FFFFFF")),
	("Burst Fade Color",("string","value=#888888")),
	("Flight Charge",(1,-128,127)),
	("Trail",False),
	("Flicker",False),
	("---------------------------------------------------------------------------------------------","label"),
	("The following items are valid for: Potion Items, ThrownPotions, Mobs","label"),
	("Potion Effect",potion_effects),
	("Potion Level",(1,-128, 127)),
	("Potion Duration (Seconds)",(0, 0, 107374181)),
	("Potion Effect has reduced particle visibility",False),
	("Potions & FW","title"),),
	
	(("Minecart Block Display:",alphaMaterials.Air),
	("Minecart Block Display Offset:",(1,-2147483648,2147483647)),
	("MinecartFurnace Fuel", (0,-32768,32767)),
	("Amount of XP per orb", (5,-32768,32767)),
	("Arrow recoverable", False),
	("Fuse Length (TNT)",(70,0,127)),
	("TNT Blast Radius", (0,-128,127)),
	("Fireball Explosion Power",(1,-2147483648,2147483647)),
	("ThrownPotion Type",splash_potions),
	("Item ID", (0,-32768,32767)),
	("Item Damage",(0,-32768,32767)),
	("Number of Items",(1,-128,127)),
	("Item Age",(0,-32768,32767)),
	("Name or Lore Operation:",("Ignore","Name","Lore")),
	("Item Name or Lore", ("string","value=")),
	("Item Enchant", enchantments),
	("Item Enchant Level", (1,-32768,32767)),
	("Item Repair Cost (-1 to ignore)",(-1,-2147483648,2147483647)),
	("Entity","title"),),
	
	(("Use Blocks in Current Selection (ignores below and air blocks)",False),
	("Falling Block ID", alphaMaterials.Air),
	("Num ticks block has been falling", (2,-128,127)),
	("Falling Block Drops Item", False),
	("Falling Block Damages Entities", False),
	("Falling Distance Damage Multiplier",2.0),
	("Max Damage From Falling Block",(20,-2147483648,2147483647)),
	("FallingSand","title"),),
	
	(("Attribute to Add or Modify:",(	"Custom",
										"generic.maxHealth",
										"generic.followRange",
										"generic.knockbackResistance",
										"generic.movementSpeed",
										"generic.attackDamage",
										"horse.jumpStrength",
										"zombie.spawnReinforcements"
									)),
	("Custom Attribute's Name:",("string","value=None")),
	("Base Value:",0.0),
	("Modifier Name:",("string","value=None")),
	("Modifier Amount:",0.0),
	("X = Attribute's Base value\nY = X, usually the Result of the previous Operation if there was one (0's result for 1, 1's result for 2, etc.)\n0: X + Amount\n1: Y + (X * Amount)\n2: Y * (1 + Amount","label"),
	("Modifier Operation:",(0,-2147483648,2147483647)),
	("\n","label"),
	("The UUID fields below are valid only for Item Attributes or for Attribute Modifiers.","label"), 
	("UUID:",("Generate Random UUID","Use UUID Least and Most","Use UUID String")),
	("UUID Least:",(0,-9223372036854775808,9223372036854775807)),
	("UUID Most:",(0,-9223372036854775808,9223372036854775807)),
	("UUID String:",("string","value=None")),
	("Attributes","title"),),
	]

def perform(level, box, options):
	slot = options["SpawnPotentials Slot"]-1
	spawntype = 1 if options["Spawner Type:"] == "Mob Spawner Block" else 0
	weight = options["Slot Weight"]
	doreplace = options["Block Replace Mode"]
	blockreplace = options["Block to (Not) Replace"]
	delay = options["Ticks Until Spawn"]
	spawndelay = options["Max Ticks Between Spawns"]
	minspawndelay = options["Min Ticks Between Spawns"]
	numspawn = options["Max Number of Entities Per Spawn"]
	maxentities = options["Maximum Spawned Entities in Area"]
	spawnrange = options["Spawning Range"]
	detectionrange = options["Player Detection Radius"]
	posmode = options["Positioning Mode"]
	autocenter = options["Auto-center X and Z to middle of block"]
	posx = options["PosX"]
	posy = options["PosY"]
	posz = options["PosZ"]
	lockspawn = options["Lock SpawnData tag"]
	usevelocity = options["Use Velocity Settings"]
	vx = options["VelocityX"]
	vy = options["VelocityY"]
	vz = options["VelocityZ"]
	fire = options["Fire"]
	fall = options["FallDistance"]

	fireworkop = options["Modify Fireworks Operation:"]
	flightduration = options["Current Rocket Flight Duration (ticks)"]
	flightdurationmax = options["Max Flight Duration Until Explosion (ticks)"]

	fireworkshape = fireworks_vals[options["Shape:"]]
	fireslot = options["Ball Slot"]-1
	fireburst = options["Burst Color"]
	firefade = options["Burst Fade Color"]
	fireflight = options["Flight Charge"]
	firetrail = options["Trail"]
	fireflicker = options["Flicker"]

	mobname = options["Mob Name"]
	mobnamevisible = options["Mob Name is visible"]
	looting = options["Can Pick Up Loot"]
	health = options["Health"]
	absorption = options["Absorption Health Amount"]
	air = options["Air"]
	attack = options["AttackTime"]
	hurt = options["HurtTime"]
	endersteal = options["Enderman is Carrying..."]
	profession = options["Villager Profession"]
	slimesize = options["Slime Size"]
	love = options["Love Mode Ticks"]
	age = options["Child/Adult Age"]
	aggro = options["Zombie Pig Aggro Level"]
	wither = options["Wither Skeleton"]
	zomvillager = options["Zombie Villager"]
	powered = options["Powered Creeper"]
	creeperradius = options["Creeper Explosion Radius"]
	creeperfuse = options["Creeper Fuse Length (ticks)"]
	ghastradius = options["Ghast Fireball Explosion Power"]
	elder = options["Elder Guardian"]
	sheepcolor = options["Sheep Wool Color"]
	rabbittype = options["Rabbit Type (99 for killer rabbit)"]
	horsetype = HorseTypes[options["Horse Type:"]]
	horsechest = options["Horse has Chest"]
	horsetame = options["Horse is Tame"]
	horsetemper = options["Horse's Temper"]
	horsevariant = options["Horse Variant:"]
	horsesaddle = options["Horse Saddle Item ID:"]
	horsearmor = options["Horse Armor Item ID:"]
	
	recover = options["Arrow recoverable"]
	fuse = options["Fuse Length (TNT)"]
	blast = options["TNT Blast Radius"]
	fireballradius = options["Fireball Explosion Power"]
	itemid = options["Item ID"]
	itemdamage = options["Item Damage"]
	numitems = options["Number of Items"]
	itemage = options["Item Age"]
	namelore = options["Item Name or Lore"]
	nameloreop = options["Name or Lore Operation:"]
	enchant = options["Item Enchant"]
	enchantlevel = options["Item Enchant Level"]
	repaircost = options["Item Repair Cost (-1 to ignore)"]
	fallid = options["Falling Block ID"]
	useselblocks = options["Use Blocks in Current Selection (ignores below and air blocks)"]
	fallticks = options["Num ticks block has been falling"]
	dodrop = options["Falling Block Drops Item"]
	damageentities = options["Falling Block Damages Entities"]
	damagemultiplier = options["Falling Distance Damage Multiplier"]
	maxdamage = options["Max Damage From Falling Block"]

	cartblock = options["Minecart Block Display:"]
	cartblockoffset = options["Minecart Block Display Offset:"]
	cartfuel = options["MinecartFurnace Fuel"]
	
	potionvalue = options["ThrownPotion Type"]
	potion = potion_effects_vals[options["Potion Effect"]]
	potionlevel = options["Potion Level"]
	potionduration = options["Potion Duration (Seconds)"]
	potionambient = options["Potion Effect has reduced particle visibility"]
	xpvalue = options["Amount of XP per orb"]
	
	defattrib = options["Attribute to Add or Modify:"]
	custattrib = options["Custom Attribute's Name:"]
	if defattrib == "Custom":
		attribname = custattrib
	else:
		attribname = defattrib
	baseval = options["Base Value:"]
	modname = options["Modifier Name:"]
	modamount = options["Modifier Amount:"]
	modop = options["Modifier Operation:"]
	uuidgen = options["UUID:"]
	uuidleast = options["UUID Least:"]
	uuidmost = options["UUID Most:"]
	uuidstr = options["UUID String:"]
	if uuidgen == "Use UUID String" and uuidstr == "None":
		uuidgen = "Generate Random UUID"

	filltype = options["Operation:"]
	if filltype == "Spawner Minecart -> Spawner" or filltype == "Entity -> Spawner":
		spawntype = 0
	else:
		spawntype = 1
	percentage = options["Number or Percentage/Grid Size"]
	mob = (options["Mob Type"] if options["Mob Type"] != "None" else (options["Entity Type"] if options["Entity Type"] != "None" else "Creeper"))
	
	tempop = options["Use Schematic:"]

	if fireburst[0] == "#":
		fireburst = int(fireburst[1:7],16)
	else:
		fireburst = 0xFFFFFF
	if firefade[0] == "#":
		firefade = int(firefade[1:7],16)
	else:
		firefade = 0x888888
	
	if mobname != "" and mobname != "None":
		mobname = mobname.encode("unicode-escape")
		mobname = mobname.replace("|",sectional)
		mobname = mobname.decode("unicode-escape")
	else:
		mobname = ""
	if namelore != "":
		namelore = namelore.encode("unicode-escape")
		namelore = namelore.replace("|",sectional)
		namelore = namelore.decode("unicode-escape")
	
	item = None
	potentials = None
	
	if filltype == "Random Fill Number":
		if (int(percentage) >= ((box.maxx-box.minx)*(box.maxz-box.minz)*(box.maxy-box.miny))):
			filltype = "Fill"
		count = int(percentage)
	elif filltype == "Grid Fill":
		count = int(percentage)+1
		
	if doreplace == "None":
		doreplace = False
		donotreplace = False
	elif doreplace == "Replace":
		doreplace = True
		donotreplace = False
	elif doreplace == "Do Not Replace":
		doreplace = True
		donotreplace = True

	if tempop and ("Fill" in filltype or filltype == "Append to SpawnPotentials Slot List" or filltype == "Prefix to SpawnPotentials Slot List"):
		template_path = mcplatform.askOpenFile(title='Select a schematic file', schematics=True)
		if template_path == None:
			print "ERROR: No schematic was selected!"
			return
		if os.path.splitext(template_path)[1] == ".schematic":
			schematic = mclevel.fromFile(template_path)
			for ent in schematic.TileEntities:
				if "id" in ent:
					if ent["id"].value == "MobSpawner":
						spawner_save = deepcopy(ent)
						if "SpawnPotentials" in spawner_save:
							potentials = spawner_save["SpawnPotentials"]
						if "SpawnData" in spawner_save:
							entity = spawner_save["SpawnData"]
						else:
							entity = TAG_Compound()
						del ent
						break
			else:
				for ent in schematic.Entities:
					if "id" in ent:
						if ent["id"].value == "MinecartSpawner":
							spawner_save = deepcopy(ent)
							if "SpawnPotentials" in spawner_save:
								potentials = spawner_save["SpawnPotentials"]
							if "SpawnData" in spawner_save:
								entity = spawner_save["SpawnData"]
							else:
								entity = TAG_Compound()
							del ent
							break
					del ent
				else:
					print "ERROR: No MobSpawners or MinecartSpawners found in schematic!"
					return
		else:
			print "ERROR: Incorrect file extension selected!"
			return
	else:
	
		if spawntype:
			spawner_save = TileEntity.Create("MobSpawner")
		else:
			spawner_save = Entity.Create("MinecartSpawner")		
		spawner_save["MinSpawnDelay"] = TAG_Short(minspawndelay if (minspawndelay < spawndelay) else spawndelay-1)
		spawner_save["MaxSpawnDelay"] = TAG_Short(spawndelay)
		spawner_save["SpawnCount"] = TAG_Short(numspawn)
		spawner_save["SpawnRange"] = TAG_Short(spawnrange)
		spawner_save["MaxNearbyEntities"] = TAG_Short(maxentities)
		spawner_save["RequiredPlayerRange"] = TAG_Short(detectionrange)
		spawner_save["Delay"] = TAG_Short(delay)
		spawner_save["EntityId"] = TAG_String(mob)
		if "Items" in spawner_save:
			del spawner_save["Items"]

		entity = Entity.Create(mob)
		entity["EntityId"] = TAG_String(mob)
		entity["Invulnerable"] = TAG_Byte(options["Invulnerable"])
		entity["Fire"] = TAG_Short(fire)
		entity["FallDistance"] = TAG_Float(fall)

		
		if mob in monsters:
		
			if not options["Use Mob's Default Health Value"]:
				entity["HealF"] = TAG_Float(health)
				
			entity["AbsorptionAmount"] = TAG_Float(absorption)
			entity["Air"] = TAG_Short(air)
			entity["AttackTime"] = TAG_Short(attack)
			entity["HurtTime"] = TAG_Short(hurt)
			entity["CanPickUpLoot"] = TAG_Byte(looting)
			entity["PersistenceRequired"] = TAG_Byte(options["Persistent (Won't Despawn)"])
			
			if mobname != "":
				entity["CustomName"] = TAG_String(mobname)
				entity["CustomNameVisible"] = TAG_Byte(mobnamevisible)
			
			if entity["id"].value == "Creeper":
				entity["powered"] = TAG_Byte(powered)
				entity["ExplosionRadius"] = TAG_Byte(creeperradius)
				entity["Fuse"] = TAG_Short(creeperfuse)

			if entity["id"].value == "Ghast":
				entity["ExplosionPower"] = TAG_Int(ghastradius)

			if entity["id"].value == "Guardian":
				entity["Elder"] = TAG_Byte(elder)
				
			if entity["id"].value == "Skeleton":
				entity["SkeletonType"] = TAG_Byte(wither)

			if entity["id"].value == "Wolf":
				entity["Angry"] = TAG_Byte(options["Angry Wolf"])

			if entity["id"].value == "Zombie":
				entity["IsVillager"] = TAG_Byte(zomvillager)
				entity["IsBaby"] = TAG_Byte(options["Baby Zombie"])

			if endersteal.ID != 0 and entity["id"].value == "Enderman":
				entity["carried"] = TAG_Short(endersteal.ID)
				entity["carriedData"] = TAG_Short(endersteal.blockData)

			if profession != "N/A" and entity["id"].value == "Villager":
				entity["Profession"] = TAG_Int(Professions[profession])

			if entity["id"].value == "Rabbit":
				entity["RabbitType"] = TAG_Int(rabbittype)

			if entity["id"].value == "Slime" or entity["id"].value == "LavaSlime":
				entity["Size"] = TAG_Int(slimesize)
				
			if entity["id"].value == "EntityHorse":
				entity["Type"] = TAG_Int(horsetype)
				entity["ChestedHorse"] = TAG_Byte(horsechest)
				if horsechest:
					entity["Items"] = TAG_List()
				entity["Tame"] = TAG_Byte(horsetame)
				entity["Temper"] = TAG_Int(horsetemper)
				entity["Variant"] = TAG_Int(horsevariant)
				if horsesaddle != 0:
					entity["SaddleItem"] = TAG_Compound()
					entity["SaddleItem"]["id"] = TAG_Short(horsesaddle)
					entity["SaddleItem"]["Damage"] = TAG_Short(0)
					entity["SaddleItem"]["Count"] = TAG_Byte(1)
				if horsearmor != 0:
					entity["ArmorItem"] = TAG_Compound()
					entity["ArmorItem"]["id"] = TAG_Short(horsearmor)
					entity["ArmorItem"]["Damage"] = TAG_Short(0)
					entity["ArmorItem"]["Count"] = TAG_Byte(1)				

			if entity["id"].value in ("Pig","Sheep","Cow","MushroomCow","Villager","Ozelot","Wolf","Chicken","EntityHorse"):
				entity["InLove"] = TAG_Int(love)
				entity["Age"] = TAG_Int(age)
				
			if entity["id"].value == "PigZombie":
				entity["Anger"] = TAG_Short(aggro);
				entity["IsBaby"] = TAG_Byte(options["Baby Zombie"])

			if entity["id"].value == "Pig":
				entity["Saddle"] = TAG_Byte(options["Saddled Pig"])

			if entity["id"].value == "Sheep":
				entity["Sheared"] = TAG_Byte(options["Shorn Sheep"])
				sheepcolor = WoolColors[sheepcolor]
				if sheepcolor > 0 and sheepcolor < 16:
					entity["Color"] = TAG_Byte(sheepcolor)

			if potion != -1:
				entity["ActiveEffects"] = TAG_List()
				ef = TAG_Compound()
				ef["Amplifier"] = TAG_Byte(potionlevel-1)
				ef["Id"] = TAG_Byte(potion)
				ef["Duration"] = TAG_Int(potionduration * 20)
				ef["Ambient"] = TAG_Byte(potionambient)
				entity["ActiveEffects"].append(ef)
		else:
			if mob == "Arrow":
				entity["pickup"] = TAG_Byte(recover)
				
			if mob == "MinecartFurnace":
				entity["Fuel"] = TAG_Short(cartfuel)

			if "Minecart" in mob:
				if cartblock.ID != 0:
					entity["DisplayTile"] = TAG_Int(cartblock.ID)
					entity["DisplayData"] = TAG_Int(cartblock.blockData)
					entity["CustomDisplayTile"] = TAG_Byte(1)
					entity["DisplayOffset"] = TAG_Int(cartblockoffset)
			
			if "Fireball" in mob or mob == "WitherSkull":
				if posmode == "Relative" or posmode == "Absolute":
					spawner_save["SpawnCount"] = TAG_Short(1)
				if not usevelocity:
					entity["Motion"] = TAG_List()
					entity["Motion"].append(TAG_Double(0.000000000000001))
					entity["Motion"].append(TAG_Double(0.000000000000001))
					entity["Motion"].append(TAG_Double(0.000000000000001))
				else:
					entity["Motion"] = TAG_List()
					entity["Motion"].append(TAG_Double(vx))
					entity["Motion"].append(TAG_Double(vy))
					entity["Motion"].append(TAG_Double(vz))
				
				entity["direction"] = TAG_List()
				entity["direction"].append(entity["Motion"][0])
				entity["direction"].append(entity["Motion"][1])
				entity["direction"].append(entity["Motion"][2])
				
				dx = entity["Motion"][0].value
				dy = entity["Motion"][1].value
				dz = entity["Motion"][2].value
				yaw = math.degrees(0 - math.atan2(dz, dx))
				pitch = math.degrees(math.sin(math.hypot(dx,dz)))
				entity["Rotation"] = TAG_List()
				entity["Rotation"].append(TAG_Float(yaw))
				entity["Rotation"].append(TAG_Float(pitch))
				
				entity["inGround"] = TAG_Byte(0)
				entity["inTile"] = TAG_Byte(0)
				entity["FallDistance"] = TAG_Float(0.0)
				entity["Fire"] = TAG_Short(20)
				entity["xTile"] = TAG_Short(-1)
				entity["yTile"] = TAG_Short(-1)
				entity["zTile"] = TAG_Short(-1)
				entity["OnGround"] = TAG_Byte(0)
				entity["ExplosionPower"] = TAG_Int(fireballradius)
				
			if mob == "PrimedTnt":
				entity["Fuse"] = TAG_Byte(fuse)
				if blast != 0:
					entity["ExplosionRadius"] = TAG_Byte(blast)

			if mob == "ThrownPotion":
				entity["Potion"] = TAG_Compound()
				entity["Potion"]["id"] = TAG_Short(373)
				entity["Potion"]["Damage"] = TAG_Short(potion_list[potionvalue])
				entity["Potion"]["Count"] = TAG_Byte(1)
				if potion != -1:
					entity["Potion"]["tag"] = TAG_Compound()
					entity["Potion"]["tag"]["CustomPotionEffects"] = TAG_List()
					addpotion = TAG_Compound()
					addpotion["Id"] = TAG_Byte(potion)
					addpotion["Amplifier"] = TAG_Byte(potionlevel-1)
					addpotion["Ambient"] = TAG_Byte(potionambient)
					addpotion["Duration"] = TAG_Int(potionduration * 20)
					entity["Potion"]["tag"]["CustomPotionEffects"].append(addpotion)
					
			if mob == "Item":
				entity["Age"] = TAG_Short(itemage)
				entity["Item"] = TAG_Compound()
				item = TAG_Compound()
				item["id"] = TAG_Short(itemid)
				item["Count"] = TAG_Byte(numitems)
				item["Damage"] = TAG_Short(itemdamage)
				if enchant != "None" or potion != -1 or (namelore != "" and nameloreop != "Ignore") or repaircost != -1 or itemid == 401 or itemid == 402:
					item["tag"] = TAG_Compound()
					if repaircost != -1:
						item["tag"]["RepairCost"] = TAG_Int(repaircost)
					if enchant != "None":
						item["tag"]["ench"] = TAG_List()
						ench = TAG_Compound()
						ench["id"] = TAG_Short(enchantment_vals[enchant])
						ench["lvl"] = TAG_Short(enchantlevel)
						item["tag"]["ench"].append(ench)
					if potion != -1:
						item["tag"]["CustomPotionEffects"] = TAG_List()
						pot = TAG_Compound()
						pot["Id"] = TAG_Byte(potion)
						pot["Amplifier"] = TAG_Byte(potionlevel-1)
						pot["Ambient"] = TAG_Byte(potionambient)
						pot["Duration"] = TAG_Int(potionduration * 20)
						item["tag"]["CustomPotionEffects"].append(pot)
					if namelore != "" and nameloreop != "Ignore":
						item["tag"]["display"] = TAG_Compound()
						if nameloreop == "Name":
							item["tag"]["display"]["Name"] = TAG_String(namelore)
						elif nameloreop == "Lore":
							item["tag"]["display"]["Lore"] = TAG_List()
							item["tag"]["display"]["Lore"].append(TAG_String(namelore))
					if itemid == 401 or itemid == 402:
						explosion = TAG_Compound()
						explosion["Flicker"] = TAG_Byte(fireflicker)
						explosion["Trail"] = TAG_Byte(firetrail)
						explosion["Type"] = TAG_Byte(fireworkshape)
						color = zeros(1,">u4")
						color[0] = fireburst
						explosion["Colors"] = TAG_Int_Array(color)
						fadecolor = zeros(1,">u4")
						fadecolor[0] = firefade
						explosion["FadeColors"] = TAG_Int_Array(fadecolor)
						if itemid == 402:
							item["tag"]["Explosion"] = explosion
						else:
							item["tag"]["Fireworks"] = TAG_Compound()
							item["tag"]["Fireworks"]["Flight"] = TAG_Byte(fireflight)
							item["tag"]["Fireworks"]["Explosions"] = TAG_List()
							item["tag"]["Fireworks"]["Explosions"].append(explosion)
				entity["Item"] = item
				
			if mob == "XPOrb":
				entity["Value"] = TAG_Short(xpvalue)
			
			if mob == "FallingSand":
				if fallid.ID in block_map:
					entity["Block"] = TAG_String(block_map[fallid.ID])
				else:
					entity["TileID"] = TAG_Int(fallid.ID)
				entity["Data"] = TAG_Byte(fallid.blockData)

				entity["Time"] = TAG_Byte(fallticks)
				entity["DropItem"] = TAG_Byte(dodrop)
				entity["HurtEntities"] = TAG_Byte(damageentities)
				entity["FallHurtAmount"] = TAG_Float(damagemultiplier)
				entity["FallHurtMax"] = TAG_Int(maxdamage)
			
			if mob == "FireworksRocketEntity":
				fwitem = TAG_Compound()
				fwitem["id"] = TAG_Short(401)
				fwitem["Count"] = TAG_Byte(numitems)
				fwitem["Damage"] = TAG_Short(itemdamage)
				fwitem["tag"] = TAG_Compound()
				fwitem["tag"]["Fireworks"] = TAG_Compound()
				fwitem["tag"]["Fireworks"]["Flight"] = TAG_Byte(fireflight)
				fwitem["tag"]["Fireworks"]["Explosions"] = TAG_List()
				explosion = TAG_Compound()
				explosion["Flicker"] = TAG_Byte(fireflicker)
				explosion["Trail"] = TAG_Byte(firetrail)
				explosion["Type"] = TAG_Byte(fireworkshape)
				color = zeros(1,">u4")
				color[0] = fireburst
				explosion["Colors"] = TAG_Int_Array(color)
				fadecolor = zeros(1,">u4")
				fadecolor[0] = firefade
				explosion["FadeColors"] = TAG_Int_Array(fadecolor)
				fwitem["tag"]["Fireworks"]["Explosions"].append(explosion)
				entity["FireworksItem"] = fwitem
				entity["Life"] = TAG_Int(flightduration)
				entity["LifeTime"] = TAG_Int(flightdurationmax)

		del entity["id"]
		del entity["EntityId"]

	if autocenter:
		posx += 0.5
		posz += 0.5

	if posmode == "Absolute":
		Entity.setpos(entity,(posx,posy,posz))
	elif posmode == "Ignore Values":
		if "Pos" in entity:
			del entity["Pos"]
	if potentials != None:
		for ent in potentials:
			if "Properties" in ent:
				if posmode == "Absolute":
					Entity.setpos(ent["Properties"],(posx,posy,posz))
				elif posmode == "Ignore Values":
					if "Pos" in ent["Properties"]:
						del ent["Properties"]["Pos"]

	if usevelocity or filltype == "Set Only Velocity":
		if "Motion" in entity:
			del entity["Motion"]
		entity["Motion"] = TAG_List()
		entity["Motion"].append(TAG_Double(vx))
		entity["Motion"].append(TAG_Double(vy))
		entity["Motion"].append(TAG_Double(vz))

	entity_save = deepcopy(entity)

	entitiesToRemove = []
	overlappingTileEntities = []
	chunkEntityCoords = []
	originalEntityList = []
	addEntityList = []
	
	def SetBlock(bx,by,bz,outer=False):
		if (bx,by,bz) in chunkEntityCoords:
			overlappingTileEntities.append((bx,by,bz))
		entity = deepcopy(entity_save)
		spawner = deepcopy(spawner_save)
		
		if useselblocks and mob == "FallingSand" and not tempop:
			e = level.tileEntityAt(x, y, z)
			if e == None:
				block = level.blockAt(x, y, z)
				data = level.blockDataAt(x, y, z)
				if block != 0:
					entity["TileID"] = TAG_Int(block)
					entity["Data"] = TAG_Byte(data)
			else:
				return
		if spawntype:
			level.setBlockAt(bx, by, bz, 52)
			TileEntity.setpos(spawner, (bx, by, bz))
		else:
			Entity.setpos(spawner, (bx+0.5, by+0.5, bz+0.5))
		if potentials != None:
			for ent in potentials:
				if "Properties" in ent:
					if posmode == "Relative":
						Entity.setpos(ent["Properties"],(bx+posx,by+posy,bz+posz))
					if ent["Type"].value == "Sheep" and sheepcolor == 16:
						ent["Properties"]["Color"] = TAG_Byte(randrange(0,15,1))

		if posmode == "Relative":
			Entity.setpos(entity,(bx+posx,by+posy,bz+posz))
		if spawner["EntityId"].value == "Sheep" and sheepcolor == 16:
			entity["Color"] = TAG_Byte(randrange(0,15,1))

		if potentials != None:
			spawner["SpawnPotentials"] = potentials
			spawner["SpawnData"] = entity
		else:
			spawner["SpawnPotentials"] = TAG_List()
			potent = TAG_Compound()
			potent["Type"] = TAG_String(spawner["EntityId"].value)
			potent["Weight"] = TAG_Int(weight)
			potent["Properties"] = deepcopy(entity)
			if "EntityId" in entity:
				del entity["EntityId"]
			spawner["SpawnData"] = entity
			spawner["SpawnPotentials"].append(potent)
			del potent

		if not spawntype:
			spawner["id"] = TAG_String("MinecartSpawner")
			spawner["Rotation"] = TAG_List([TAG_Float(0.0), TAG_Float(0.0)])
			spawner["Motion"] = TAG_List([TAG_Double(0.0), TAG_Double(0.0), TAG_Double(0.0)])
			spawner["OnGround"] = TAG_Byte(0)
			spawner["Fire"] = TAG_Short(-1)
			spawner["Dimension"] = TAG_Int(0)
			spawner["PortalCooldown"] = TAG_Int(0)
			spawner["FallDistance"] = TAG_Float(0)
			spawner["Air"] = TAG_Short(0)
			spawner["Invulnerable"] = TAG_Byte(0)
			
		if not outer:
			if spawntype:
				chunk.TileEntities.append(spawner)
			else:
				chunk.Entities.append(spawner)				
		else:
			addEntityList.append(spawner)
	randnumlist = []
	
	if filltype == "List SpawnPotentials Slots in Console":
		print "\nPrinting a list of all spawner SpawnPotentials Slots within selection...."
	
	for (chunk, _, _) in level.getChunkSlices(box):
		chunkEntityCoords = []
		(cx,cz) = chunk.chunkPosition
		cposx = cx * 16
		cposz = cz * 16
		if "Fill" in filltype:
			if spawntype:
				for entity in chunk.TileEntities:
					ex = entity["x"].value
					ey = entity["y"].value
					ez = entity["z"].value
					if (ex,ey,ez) in box:
						chunkEntityCoords.append((ex,ey,ez))
						originalEntityList.append(entity)
			if filltype == "Fill":
				for y in range(box.miny,box.maxy,1):
					for x in range((cposx if (cposx > box.minx) else box.minx),(cposx+16 if ((cposx+16) < box.maxx) else box.maxx),1):
						for z in range((cposz if (cposz > box.minz) else box.minz),(cposz+16 if((cposz+16) < box.maxz) else box.maxz),1):
							if not doreplace:
								SetBlock(x,y,z)
							elif doreplace and not donotreplace and level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData:
								SetBlock(x,y,z)
							elif donotreplace and not (level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData):
								SetBlock(x,y,z)
			elif filltype == "Grid Fill":
				for y in range(box.miny,box.maxy,count):
					for x in range(cposx+((box.minx-cposx)%count),cposx+16,count):
						for z in range(cposz+((box.minz-cposz)%count),cposz+16,count):
							if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
								if not doreplace:
									SetBlock(x,y,z)
								elif doreplace and not donotreplace and level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData:
									SetBlock(x,y,z)
								elif donotreplace and not (level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData):
									SetBlock(x,y,z)

			for oldentity in originalEntityList:
				ox = oldentity["x"].value
				oy = oldentity["y"].value
				oz = oldentity["z"].value
				if (ox,oy,oz) in overlappingTileEntities:
					entitiesToRemove.append((chunk, oldentity))
			
			chunk.dirty = True
			
			overlappingTileEntities[:] = []
			originalEntityList[:] = []
			chunkEntityCoords[:] = []
		else:
			for entity in chunk.TileEntities if spawntype else chunk.Entities:
				if spawntype:
					x = entity["x"].value
					y = entity["y"].value
					z = entity["z"].value
				else:
					x = entity["Pos"][0].value
					y = entity["Pos"][1].value
					z = entity["Pos"][2].value

				if "id" not in entity:
					continue
				if entity["id"].value != "MobSpawner" and (entity["id"].value != "MinecartSpawner" or filltype == "Entity -> Spawner"):
					if filltype == "TileEntity -> FallingSand Spawner" and spawntype:
						if (x,y,z) in box:
							fallsand = TAG_Compound()
							fallsand["id"] = TAG_String("FallingSand")
							tileid = level.blockAt(x,y,z)
							if tileid in block_map:
								fallsand["Block"] = TAG_String(block_map[tileid])
							else:
								fallsand["TileID"] = TAG_Int(tileid)
							fallsand["Data"] = TAG_Byte(level.blockDataAt(x,y,z))
							fallsand["TileEntityData"] = deepcopy(entity)
							fallsand["DropItem"] = TAG_Byte(dodrop)
							fallsand["Time"] = TAG_Byte(fallticks)
							fallsand["HurtEntities"] = TAG_Byte(damageentities)
							fallsand["FallHurtMax"] = TAG_Int(maxdamage)
							fallsand["FallHurtAmount"] = TAG_Float(damagemultiplier)
							for val in entity.keys():
								if val != "x" and val != "y" and val != "z":
									del entity[val]							
							entity["id"] = TAG_String("MobSpawner")
							if not lockspawn:
								if "SpawnData" in entity:
									del entity["SpawnData"]
							if "SpawnPotentials" in entity:
								del entity["SpawnPotentials"]
							entity["SpawnPotentials"] = TAG_List()

							newpot = TAG_Compound()
							newpot["Weight"] = TAG_Int(weight)
							newpot["Type"] = TAG_String("FallingSand")
							newpot["Properties"] = fallsand
							entity["SpawnPotentials"].append(newpot)
							
							entity["MinSpawnDelay"] = TAG_Short(minspawndelay if (minspawndelay < spawndelay) else spawndelay-1)
							entity["MaxSpawnDelay"] = TAG_Short(spawndelay)
							entity["SpawnCount"] = TAG_Short(numspawn)
							entity["SpawnRange"] = TAG_Short(spawnrange)
							entity["MaxNearbyEntities"] = TAG_Short(maxentities)
							entity["RequiredPlayerRange"] = TAG_Short(detectionrange)
							entity["Delay"] = TAG_Short(delay)
							
							level.setBlockAt(x, y, z, 52)
							level.setBlockDataAt(x, y, z, 0)
							
							del fallsand
							del newpot
							chunk.dirty = True
					elif filltype == "Entity -> Spawner" and not spawntype:
						if (x,y,z) in box:
							if "UUIDMost" in entity:
								del entity["UUIDMost"]
							if "UUIDLeast" in entity:
								del entity["UUIDLeast"]
							spawn = TAG_Compound()
							spawn["id"] = TAG_String("MobSpawner")
							spawn["SpawnPotentials"] = TAG_List()
							if posmode == "Relative":
								newx = int(math.floor(x))
								newy = int(math.floor(y))
								newz = int(math.floor(z))
								Entity.setpos(entity,(newx+posx,newy+posy,newz+posz))
							elif posmode == "Absolute":
								Entity.setpos(entity,(posx,posy,posz))
							else:
								if "Pos" in entity:
									del entity["Pos"]
							newpot = TAG_Compound()
							newpot["Weight"] = TAG_Int(weight)
							newpot["Type"] = TAG_String(entity["id"].value)
							newpot["Properties"] = deepcopy(entity)
							spawn["SpawnPotentials"].append(newpot)
							spawn["SpawnData"] = deepcopy(entity)
							
							spawn["MinSpawnDelay"] = TAG_Short(minspawndelay if (minspawndelay < spawndelay) else spawndelay-1)
							spawn["MaxSpawnDelay"] = TAG_Short(spawndelay)
							spawn["SpawnCount"] = TAG_Short(numspawn)
							spawn["SpawnRange"] = TAG_Short(spawnrange)
							spawn["MaxNearbyEntities"] = TAG_Short(maxentities)
							spawn["RequiredPlayerRange"] = TAG_Short(detectionrange)
							spawn["Delay"] = TAG_Short(delay)
							spawn["EntityId"] = TAG_String(entity["id"].value)
							
							TileEntity.setpos(spawn, (int(math.floor(x)), int(math.floor(y)), int(math.floor(z))))
							chunk.TileEntities.append(spawn)
							entitiesToRemove.append((chunk,entity))
							level.setBlockAt(int(math.floor(x)), int(math.floor(y)), int(math.floor(z)), 52)
							level.setBlockDataAt(int(math.floor(x)), int(math.floor(y)), int(math.floor(z)), 0)
							
							del spawn
							del newpot
							chunk.dirty = True
							continue
					else:
						continue
				if (x,y,z) in box:
					if "SpawnPotentials" not in entity:
						entity["SpawnPotentials"] = TAG_List()
						potent = TAG_Compound()
						potent["Type"] = TAG_String(entity["EntityId"].value)
						potent["Weight"] = TAG_Int(weight)
						if "SpawnData" in entity:
							potent["Properties"] = deepcopy(entity["SpawnData"])
						elif filltype != "Append to SpawnPotentials Slot List" and filltype != "Prefix to SpawnPotentials Slot List":
							potent["Properties"] = entity_save
						entity["SpawnPotentials"].append(potent)
						del potent

					if filltype == "Append to SpawnPotentials Slot List" or filltype == "Prefix to SpawnPotentials Slot List":
						if potentials == None:
							newpot = TAG_Compound()
							newpot["Weight"] = TAG_Int(weight)
							newpot["Type"] = TAG_String(spawner_save["EntityId"].value)
							newpot["Properties"] = entity_save
							if posmode == "Relative":
								Entity.setpos(newpot["Properties"],(x+posx,y+posy,z+posz))
							elif posmode == "Absolute":
								Entity.setpos(newpot["Properties"],(posx,posy,posz))
							else:
								if "Pos" in newpot["Properties"]:
									del newpot["Properties"]["Pos"]
							if filltype == "Append to SpawnPotentials Slot List":
								entity["SpawnPotentials"].append(newpot)
							else:
								entity["SpawnPotentials"].insert(0,newpot)
							del newpot
						else:
							for po in potentials:
								if posmode == "Relative":
									Entity.setpos(po["Properties"],(x+posx,y+posy,z+posz))
								elif posmode == "Absolute":
									Entity.setpos(po["Properties"],(posx,posy,posz))
								else:
									if "Pos" in po["Properties"]:
										del po["Properties"]["Pos"]
								if filltype == "Append to SpawnPotentials Slot List":
									entity["SpawnPotentials"].append(po)
								else:
									entity["SpawnPotentials"].insert(0,po)
					elif filltype == "Bring SpawnPotentials Slot to Front":
						if slot <= len(entity["SpawnPotentials"]) and slot > 0:
							entity["SpawnPotentials"].insert(0,entity["SpawnPotentials"].pop(slot))
						else:
							continue
					elif filltype == "List SpawnPotentials Slots in Console":
						slotcounter = 0
						print "Spawner at: "+str(x)+", "+str(y)+", "+str(z)
						for ent in entity["SpawnPotentials"]:
							slotcounter += 1
							print str(slotcounter)+": "+ str(ent["Type"].value),
							if "Riding" in ent["Properties"]:
								iterent = ent["Properties"]["Riding"]
								while True:
									print "riding "+str(iterent["id"].value),
									if "Riding" not in iterent:
										break
									iterent = iterent["Riding"]			
							print ", weight: "+str(ent["Weight"].value)
					elif filltype == "Spawner -> Falling Spawner":
						if entity["id"].value != "MobSpawner":
							continue
						fallsand = TAG_Compound()
						fallsand["id"] = TAG_String("FallingSand")
						fallsand["Block"] = TAG_String(block_map[52])
						fallsand["TileID"] = TAG_Int(52)
						fallsand["Data"] = TAG_Byte(0)
						fallsand["TileEntityData"] = deepcopy(entity)
						fallsand["DropItem"] = TAG_Byte(dodrop)
						fallsand["Time"] = TAG_Byte(fallticks)
						fallsand["HurtEntities"] = TAG_Byte(damageentities)
						fallsand["FallHurtMax"] = TAG_Int(maxdamage)
						fallsand["FallHurtAmount"] = TAG_Float(damagemultiplier)
						if not lockspawn:
							if "SpawnData" in entity:
								del entity["SpawnData"]
						if "SpawnPotentials" in entity:
							del entity["SpawnPotentials"]
						entity["SpawnPotentials"] = TAG_List()

						newpot = TAG_Compound()
						newpot["Weight"] = TAG_Int(weight)
						newpot["Type"] = TAG_String("FallingSand")
						newpot["Properties"] = fallsand
						entity["SpawnPotentials"].append(newpot)
						
						entity["MinSpawnDelay"] = TAG_Short(minspawndelay if (minspawndelay < spawndelay) else spawndelay-1)
						entity["MaxSpawnDelay"] = TAG_Short(spawndelay)
						entity["SpawnCount"] = TAG_Short(numspawn)
						entity["SpawnRange"] = TAG_Short(spawnrange)
						entity["MaxNearbyEntities"] = TAG_Short(maxentities)
						entity["RequiredPlayerRange"] = TAG_Short(detectionrange)
						entity["Delay"] = TAG_Short(delay)
						del fallsand
						del newpot
						chunk.dirty = True


					elif filltype == "Spawner -> Spawner Minecart":
						if entity["id"].value != "MobSpawner":
							continue
						spwn = deepcopy(entity)
						spwn["id"] = TAG_String("MinecartSpawner")
						spwn["Rotation"] = TAG_List([TAG_Float(0.0), TAG_Float(0.0)])
						spwn["Motion"] = TAG_List([TAG_Double(0.0), TAG_Double(0.0), TAG_Double(0.0)])
						spwn["OnGround"] = TAG_Byte(0)
						spwn["Fire"] = TAG_Short(-1)
						spwn["Dimension"] = TAG_Int(0)
						spwn["PortalCooldown"] = TAG_Int(0)
						spwn["FallDistance"] = TAG_Float(0)
						spwn["Air"] = TAG_Short(0)
						spwn["Invulnerable"] = TAG_Byte(0)
						if "x" in spwn:
							del spwn["x"]
						if "y" in spwn:
							del spwn["y"]
						if "z" in spwn:
							del spwn["z"]
							
						if cartblock.ID != 0:
							spwn["DisplayTile"] = TAG_Int(cartblock.ID)
							spwn["DisplayData"] = TAG_Int(cartblock.blockData)
							spwn["CustomDisplayTile"] = TAG_Byte(1)
							spwn["DisplayOffset"] = TAG_Int(cartblockoffset)
						Entity.setpos(spwn, (x+0.5, y+0.5, z+0.5))
						chunk.Entities.append(spwn)
						entitiesToRemove.append((chunk,entity))
						level.setBlockAt(x, y, z, 0)
						del spwn
						chunk.dirty = True
					elif filltype == "Spawner Minecart -> Spawner":
						if entity["id"].value != "MinecartSpawner":
							continue
						if "UUIDMost" in entity:
							del entity["UUIDMost"]
						if "UUIDLeast" in entity:
							del entity["UUIDLeast"]
						spwn = deepcopy(entity)
						spwn["id"] = TAG_String("MobSpawner")
						if "Rotation" in spwn:
							del spwn["Rotation"]
						if "Motion" in spwn:
							del spwn["Motion"]
						if "OnGround" in spwn:
							del spwn["OnGround"]
						if "Fire" in spwn:
							del spwn["Fire"]
						if "Dimension" in spwn:
							del spwn["Dimension"]
						if "PortalCooldown" in spwn:
							del spwn["PortalCooldown"]
						if "FallDistance" in spwn:
							del spwn["FallDistance"]
						if "Air" in spwn:
							del spwn["Air"]
						if "Invulnerable" in spwn:
							del spwn["Invulnerable"]
						if "Pos" in spwn:
							del spwn["Pos"]
						if "DisplayTile" in spwn:
							del spwn["DisplayTile"]
						if "DisplayData" in spwn:
							del spwn["DisplayData"]
						if "CustomDisplayTile" in spwn:
							del spwn["CustomDisplayTile"]
						if "DisplayOffset" in spwn:
							del spwn["DisplayOffset"]

						TileEntity.setpos(spwn, (int(math.floor(x)), int(math.floor(y)), int(math.floor(z))))
						chunk.TileEntities.append(spwn)
						entitiesToRemove.append((chunk,entity))
						level.setBlockAt(int(math.floor(x)), int(math.floor(y)), int(math.floor(z)), 52)
						chunk.dirty = True
						del spwn
					elif filltype == "Stack SpawnPotentials Slots into Riding Entities":
						if "SpawnPotentials" not in entity:
							continue
						ridingent = TAG_Compound()
						start = 0
						for pot in entity["SpawnPotentials"]:
							if start == 0:
								ridingent = deepcopy(pot["Properties"])
								ridingent["id"] = TAG_String(pot["Type"].value)
								nextent = ridingent
								start = 1
							else:
								nextent["Riding"] = deepcopy(pot["Properties"])
								nextent["Riding"]["id"] = TAG_String(pot["Type"].value)
								nextent = nextent["Riding"]
						del entity["SpawnPotentials"]
						entity["SpawnPotentials"] = TAG_List()
						newpot = TAG_Compound()
						newpot["Type"] = TAG_String(ridingent["id"].value)
						newpot["Weight"] = TAG_Int(weight)
						newpot["Properties"] = deepcopy(ridingent)
						entity["SpawnPotentials"].append(newpot)
						if not lockspawn:
							if "SpawnData" in entity:
								del entity["SpawnData"]
							entity["SpawnData"] = deepcopy(ridingent)
						del newpot
						del nextent
						del ridingent
					elif filltype == "Unstack Riding Entities into SpawnPotentials Slots":
						if "SpawnPotentials" not in entity:
							continue
						entslist = TAG_List()
						for pot in entity["SpawnPotentials"]:
							iterate = pot["Properties"]
							while True:
								newiterate = deepcopy(iterate)
								if "Riding" in newiterate:
									del newiterate["Riding"]
								if "id" not in newiterate:
									newiterate["id"] = TAG_String(pot["Type"].value)
								entslist.append(newiterate)
								if "Riding" not in iterate:
									break
								iterate = iterate["Riding"]
						del entity["SpawnPotentials"]
						if not lockspawn:
							if "SpawnData" in entity:
								del entity["SpawnData"]
						entity["SpawnPotentials"] = TAG_List()
						for en in entslist:
							newpot = TAG_Compound()
							newpot["Type"] = TAG_String(en["id"].value)
							newpot["Weight"] = TAG_Int(weight)
							newpot["Properties"] = deepcopy(en)
							entity["SpawnPotentials"].append(newpot)
						if not lockspawn:
							entity["SpawnData"] = deepcopy(entity["SpawnPotentials"][0]["Properties"])
							entity["EntityId"] = TAG_String(entity["SpawnPotentials"][0]["Type"].value)
						
						del newpot
						del entslist
						del iterate
						del newiterate
						
					if len(entity["SpawnPotentials"])-1 < slot:
						continue

					if "Clear" in filltype:
						if filltype == "Clear All Properties":
							for a in entity.keys():
								if a != "id" and a != "x" and a != "y" and a != "z" and a != "EntityId":
									del entity[a]
						elif filltype == "Clear Potion Effects":
							if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
								if "tag" in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									if "CustomPotionEffects" in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
										del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["CustomPotionEffects"]
							elif "Potion" in entity["SpawnPotentials"][slot]["Properties"]:
								if "tag" in entity["SpawnPotentials"][slot]["Properties"]["Potion"]:
									if "CustomPotionEffects" in entity["SpawnPotentials"][slot]["Properties"]["Potion"]["tag"]:
										del entity["SpawnPotentials"][slot]["Properties"]["Potion"]["tag"]["CustomPotionEffects"]
							elif "ActiveEffects" in entity["SpawnPotentials"][slot]["Properties"]:
								del entity["SpawnPotentials"][slot]["Properties"]["ActiveEffects"]
						elif filltype == "Clear Enchants":
							if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
								if "tag" in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									if "ench" in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
										del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["ench"]
						elif filltype == "Clear Name":
							if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
								if "tag" in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									if "display" in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
										if "Name" in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"]:
											del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"]["Name"]
						elif filltype == "Clear Lores":
							if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
								if "tag" in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									if "display" in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
										if "Lore" in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"]:
											del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"]["Lore"]
						elif filltype == "Clear SpawnPotentials Slot":
							del entity["SpawnPotentials"][slot]
						elif filltype == "Clear Attributes (Mobs Only)":
							if "Attributes" in entity["SpawnPotentials"][slot]["Properties"]:
								del entity["SpawnPotentials"][slot]["Properties"]["Attributes"]
						elif filltype == "Clear Attribute Modifiers (Item Entities Only)":
							if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
								if "tag" in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									if "AttributeModifiers" in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
										del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["AttributeModifiers"]
							
					elif filltype == "Modify Fireworks":
						if fireworkop == "List all Fireworks Balls in Rocket":
							if entity["SpawnPotentials"][slot]["Type"].value == "Item":
								if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
									if entity["SpawnPotentials"][slot]["Properties"]["Item"]["id"].value != 401:
										continue
									if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
										continue
									if "Fireworks" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
										continue
									if "Explosions" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]:
										continue
									slotcounter = 0
									print "Spawner at: X "+str(x)+", Y "+str(y)+", Z "+str(z)+", Spawner slot: "+str(slot+1)+", weight: "+str(entity["SpawnPotentials"][slot]["Weight"].value)
									for ent in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"]:
										slotcounter += 1
										print (str(slotcounter)+": "+ str(fireworks[ent["Type"].value])),
										if "Colors" in ent:
											color = ent["Colors"].value
											print (" Color(s): "),
											for i in color:
												val = hex(int(i))[2:]
												val = val.zfill(6)
												print ("#"+val+", "),
										if "FadeColors" in ent:
											color = ent["FadeColors"].value
											print (" Fade Color(s): "),
											for i in color:
												val = hex(int(i))[2:]
												val = val.zfill(6)
												print ("#"+val+", "),
										print ""
							elif entity["SpawnPotentials"][slot]["Type"].value == "FireworksRocketEntity":
								if "FireworksItem" in entity["SpawnPotentials"][slot]["Properties"]:
									if entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["id"].value != 401:
										continue
									if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]:
										continue
									if "Fireworks" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]:
										continue
									if "Explosions" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]:
										continue
									slotcounter = 0
									print "Spawner at: X "+str(x)+", Y "+str(y)+", Z "+str(z)+", Spawner slot: "+str(slot+1)+", weight: "+str(entity["SpawnPotentials"][slot]["Weight"].value)
									for ent in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"]:
										slotcounter += 1
										print (str(slotcounter)+": "+ str(fireworks[ent["Type"].value])),
										if "Colors" in ent:
											color = ent["Colors"].value
											print (" Color(s): "),
											for i in color:
												val = hex(int(i))[2:]
												val = val.zfill(6)
												print ("#"+val+", "),
										if "FadeColors" in ent:
											color = ent["FadeColors"].value
											print ("Fade Color(s): "),
											for i in color:
												val = hex(int(i))[2:]
												val = val.zfill(6)
												print ("#"+val+", "),
										print ""
						elif fireworkop == "Add Burst Color to Ball" or fireworkop == "Add Fade Color to Ball":
							if entity["SpawnPotentials"][slot]["Type"].value == "Item":
								if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
									if entity["SpawnPotentials"][slot]["Properties"]["Item"]["id"].value != 401 and entity["SpawnPotentials"][slot]["Properties"]["Item"]["id"].value != 402:
										continue
									if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
										continue
									if entity["SpawnPotentials"][slot]["Properties"]["Item"]["id"].value == 401:
										if "Fireworks" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
											continue
										if "Explosions" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]:
											continue
										if len(entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"])-1 < fireslot:
											continue
										if fireworkop == "Add Burst Color to Ball":
											if "Colors" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]:
												color = zeros(1,">u4")
												color[0] = fireburst
												entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]["Colors"] = TAG_Int_Array(color)
											else:
												color = entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]["Colors"].value
												color = append(color,fireburst)
												newcolor = fromiter(color,">u4")
												del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]["Colors"]
												entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]["Colors"] = TAG_Int_Array(newcolor)
										elif fireworkop == "Add Fade Color to Ball":
											if "FadeColors" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]:
												color = zeros(1,">u4")
												color[0] = firefade
												entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]["FadeColors"] = TAG_Int_Array(color)
											else:
												color = entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]["FadeColors"].value
												color = append(color,firefade)
												newcolor = fromiter(color,">u4")
												del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]["FadeColors"]
												entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]["FadeColors"] = TAG_Int_Array(newcolor)
									elif entity["SpawnPotentials"][slot]["Properties"]["Item"]["id"].value == 402:
										if "Explosion" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
											continue
										if fireworkop == "Add Burst Color to Ball":
											if "Colors" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]:
												color = zeros(1,">u4")
												color[0] = fireburst
												entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]["Colors"] = TAG_Int_Array(color)
											else:
												color = entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]["Colors"].value
												color = append(color,fireburst)
												newcolor = fromiter(color,">u4")
												del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]["Colors"]
												entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]["Colors"] = TAG_Int_Array(newcolor)
										elif fireworkop == "Add Fade Color to Ball":
											if "FadeColors" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]:
												color = zeros(1,">u4")
												color[0] = firefade
												entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]["FadeColors"] = TAG_Int_Array(color)
											else:
												color = entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]["FadeColors"].value
												color = append(color,firefade)
												newcolor = fromiter(color,">u4")
												del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]["FadeColors"]
												entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Explosion"]["FadeColors"] = TAG_Int_Array(newcolor)
							elif entity["SpawnPotentials"][slot]["Type"].value == "FireworksRocketEntity":
								if "FireworksItem" in entity["SpawnPotentials"][slot]["Properties"]:
									if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]:
										continue
									if "Fireworks" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]:
										continue
									if "Explosions" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]:
										continue
									if len(entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"])-1 < fireslot:
										continue
									if fireworkop == "Add Burst Color to Ball":
										if "Colors" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]:
											color = zeros(1,">u4")
											color[0] = fireburst
											entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]["Colors"] = TAG_Int_Array(color)
										else:
											color = entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]["Colors"].value
											color = append(color,fireburst)
											newcolor = fromiter(color,">u4")
											del entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]["Colors"]
											entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]["Colors"] = TAG_Int_Array(newcolor)
									elif fireworkop == "Add Fade Color to Ball":
										if "FadeColors" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]:
											color = zeros(1,">u4")
											color[0] = firefade
											entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]["FadeColors"] = TAG_Int_Array(color)
										else:
											color = entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]["FadeColors"].value
											color = append(color,firefade)
											newcolor = fromiter(color,">u4")
											del entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]["FadeColors"]
											entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]["FadeColors"] = TAG_Int_Array(newcolor)
						elif fireworkop == "Clear Fireworks Ball from Rocket":
							if entity["SpawnPotentials"][slot]["Type"].value == "Item":
								if "Item" not in entity["SpawnPotentials"][slot]["Properties"]:
									continue
								if entity["SpawnPotentials"][slot]["Properties"]["Item"]["id"].value != 401:
									continue
								if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									continue
								if "Fireworks" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
									continue
								if "Explosions" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]:
									continue
								if len(entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"])-1 < fireslot:
									continue
								del entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"][fireslot]
							elif entity["SpawnPotentials"][slot]["Type"].value == "FireworksRocketEntity":
								if "FireworksItem" not in entity["SpawnPotentials"][slot]["Properties"]:
									continue
								if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]:
									continue
								if "Fireworks" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]:
									continue
								if "Explosions" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]:
									continue
								if len(entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"])-1 < fireslot:
									continue
								del entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"][fireslot]
						elif fireworkop == "Add Fireworks Ball to Rocket":
							if entity["SpawnPotentials"][slot]["Type"].value == "Item":
								if "Item" not in entity["SpawnPotentials"][slot]["Properties"]:
									continue
								if entity["SpawnPotentials"][slot]["Properties"]["Item"]["id"].value != 401:
									continue
								if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									continue
								if "Fireworks" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
									continue
								if "Explosions" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]:
									continue
								if len(entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"])-1 < fireslot:
									continue
								explosion = TAG_Compound()
								explosion["Flicker"] = TAG_Byte(fireflicker)
								explosion["Trail"] = TAG_Byte(firetrail)
								explosion["Type"] = TAG_Byte(fireworkshape)
								color = zeros(1,">u4")
								color[0] = fireburst
								explosion["Colors"] = TAG_Int_Array(color)
								fadecolor = zeros(1,">u4")
								fadecolor[0] = firefade
								explosion["FadeColors"] = TAG_Int_Array(fadecolor)
								entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["Fireworks"]["Explosions"].append(explosion)
							elif entity["SpawnPotentials"][slot]["Type"].value == "FireworksRocketEntity":
								if "FireworksItem" not in entity["SpawnPotentials"][slot]["Properties"]:
									continue
								if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]:
									continue
								if "Fireworks" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]:
									continue
								if "Explosions" not in entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]:
									continue
								if len(entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"])-1 < fireslot:
									continue
								explosion = TAG_Compound()
								explosion["Flicker"] = TAG_Byte(fireflicker)
								explosion["Trail"] = TAG_Byte(firetrail)
								explosion["Type"] = TAG_Byte(fireworkshape)
								color = zeros(1,">u4")
								color[0] = fireburst
								explosion["Colors"] = TAG_Int_Array(color)
								fadecolor = zeros(1,">u4")
								fadecolor[0] = firefade
								explosion["FadeColors"] = TAG_Int_Array(fadecolor)
								entity["SpawnPotentials"][slot]["Properties"]["FireworksItem"]["tag"]["Fireworks"]["Explosions"].append(explosion)
						elif fireworkop == "Set Rocket Flight and Max Rocket Flight Duration":
							if entity["SpawnPotentials"][slot]["Type"].value == "FireworksRocketEntity":
								entity["SpawnPotentials"][slot]["Properties"]["Life"] = TAG_Int(flightduration)
								entity["SpawnPotentials"][slot]["Properties"]["LifeTime"] = TAG_Int(flightdurationmax)
					elif filltype == "Set SpawnPotentials Slot Weight":
						entity["SpawnPotentials"][slot]["Weight"] = TAG_Int(weight)
					elif filltype == "Set SpawnPotentials Slot as Active Spawn":
						if "SpawnData" in entity:
							del entity["SpawnData"]
						entity["SpawnData"] = entity["SpawnPotentials"][slot]["Properties"]
						entity["EntityId"] = TAG_String(entity["SpawnPotentials"][slot]["Type"].value)
					elif filltype == "Add New Properties for \"Entity\\Mob Type\"":
						if entity["SpawnPotentials"][slot]["Type"].value == mob:
							for val in spawner_save.keys():
								if val != "x" and val != "y" and val != "z" and type(spawner_save[val]) is not TAG_Compound and type(spawner_save[val]) is not TAG_List:
									entity[val] = spawner_save[val]

							for e in entity_save.keys():
								if e == "Pos":
									if posmode == "Relative":
										Entity.setpos(entity["SpawnPotentials"][slot]["Properties"],(x+posx,y+posy,z+posz))
									elif posmode == "Absolute":
										entity["SpawnPotentials"][slot]["Properties"]["Pos"] = entity_save["Pos"]
								elif type(entity_save[e]) is TAG_Compound or type(entity_save[e]) is TAG_List:
									continue
								else:
									entity["SpawnPotentials"][slot]["Properties"][e] = entity_save[e]
						
					elif filltype == "Add Potion Effect":
						if potion != -1:
							if entity["SpawnPotentials"][slot]["Type"].value in monsters:
								if "ActiveEffects" not in entity["SpawnPotentials"][slot]["Properties"]:
									entity["SpawnPotentials"][slot]["Properties"]["ActiveEffects"] = TAG_List()
								ef = TAG_Compound()
								ef["Amplifier"] = TAG_Byte(potionlevel-1)
								ef["Ambient"] = TAG_Byte(potionambient)
								ef["Id"] = TAG_Byte(potion)
								ef["Duration"] = TAG_Int(potionduration * 20)
								entity["SpawnPotentials"][slot]["Properties"]["ActiveEffects"].append(ef)
								del ef
							elif entity["SpawnPotentials"][slot]["Type"].value == "Item":
								if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
									if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
										entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"] = TAG_Compound()
									if "CustomPotionEffects" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
										entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["CustomPotionEffects"] = TAG_List()
									pot = TAG_Compound()
									pot["Id"] = TAG_Byte(potion)
									pot["Amplifier"] = TAG_Byte(potionlevel-1)
									pot["Ambient"] = TAG_Byte(potionambient)
									pot["Duration"] = TAG_Int(potionduration * 20)
									entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["CustomPotionEffects"].append(pot)
									del pot											
							elif entity["SpawnPotentials"][slot]["Type"].value == "ThrownPotion":
								if "Potion" in entity["SpawnPotentials"][slot]["Properties"]:
									if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Potion"]:
										entity["SpawnPotentials"][slot]["Properties"]["Potion"]["tag"] = TAG_Compound()
									if "CustomPotionEffects" not in entity["SpawnPotentials"][slot]["Properties"]["Potion"]["tag"]:
										entity["SpawnPotentials"][slot]["Properties"]["Potion"]["tag"]["CustomPotionEffects"] = TAG_List()
									pot = TAG_Compound()
									pot["Id"] = TAG_Byte(potion)
									pot["Amplifier"] = TAG_Byte(potionlevel-1)
									pot["Ambient"] = TAG_Byte(potionambient)
									pot["Duration"] = TAG_Int(potionduration * 20)
									entity["SpawnPotentials"][slot]["Properties"]["Potion"]["tag"]["CustomPotionEffects"].append(pot)
									del pot											
					elif filltype == "Add Enchant":
						if entity["SpawnPotentials"][slot]["Type"].value == "Item" and enchant != "None":
							if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
								if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"] = TAG_Compound()
								if "ench" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
									entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["ench"] = TAG_List()
								tempenchant = TAG_Compound()
								tempenchant["id"] = TAG_Short(enchantment_vals[enchant])
								tempenchant["lvl"] = TAG_Short(enchantlevel)
								if repaircost != -1:
									entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["RepairCost"] = TAG_Int(repaircost)
								entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["ench"].append(tempenchant)
								del tempenchant
					elif filltype == "Set Mob Name Properties":
						if entity["SpawnPotentials"][slot]["Type"].value in monsters:
							entity["SpawnPotentials"][slot]["Properties"]["CustomNameVisible"] = TAG_Byte(mobnamevisible)
							if mobname == "" or mobname == "None":
								entity["SpawnPotentials"][slot]["Properties"]["CustomName"] = TAG_String()
							else:
								entity["SpawnPotentials"][slot]["Properties"]["CustomName"] = TAG_String(mobname)
					elif filltype == "Set Name":
						if entity["SpawnPotentials"][slot]["Type"].value == "Item" and namelore != "":
							if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
								if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"] = TAG_Compound()
								if "display" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
									entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"] = TAG_Compound()
								entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"]["Name"] = TAG_String(namelore)
					elif filltype == "Add Lore":
						if entity["SpawnPotentials"][slot]["Type"].value == "Item" and namelore != "":
							if "Item" in entity["SpawnPotentials"][slot]["Properties"]:
								if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
									entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"] = TAG_Compound()
								if "display" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
									entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"] = TAG_Compound()
								if "Lore" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"]:
									entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"]["Lore"] = TAG_List()
								entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["display"]["Lore"].append(TAG_String(namelore))
					elif filltype == "Set Only Velocity":
						entity["SpawnPotentials"][slot]["Properties"]["Motion"] = entity_save["Motion"]
					elif filltype == "Set Only Position":
						if posmode == "Relative":
							Entity.setpos(entity["SpawnPotentials"][slot]["Properties"],(x+posx,y+posy,z+posz))
						elif posmode == "Absolute":
							Entity.setpos(entity["SpawnPotentials"][slot]["Properties"],(posx,posy,posz))
						else:
							if "Pos" in entity["SpawnPotentials"][slot]["Properties"]:
								del entity["SpawnPotentials"][slot]["Properties"]["Pos"]
					elif filltype == "Set Only Spawn Conditions":
						entity["MinSpawnDelay"] = spawner_save["MinSpawnDelay"]
						entity["MaxSpawnDelay"] = spawner_save["MaxSpawnDelay"]
						entity["SpawnCount"] = spawner_save["SpawnCount"]
						entity["Delay"] = spawner_save["Delay"]
						entity["SpawnRange"] = spawner_save["SpawnRange"]
						entity["MaxNearbyEntities"] = spawner_save["MaxNearbyEntities"]
						entity["RequiredPlayerRange"] = spawner_save["RequiredPlayerRange"]
						
					elif filltype == "Add or Edit Attribute (Mobs Only)":
						if "Attributes" not in entity["SpawnPotentials"][slot]["Properties"]:
							entity["SpawnPotentials"][slot]["Properties"]["Attributes"] = TAG_List()
						for a in entity["SpawnPotentials"][slot]["Properties"]["Attributes"]:
							if a["Name"].value == attribname:
								a["Base"] = TAG_Double(baseval)
								break
						else:
							attrib = TAG_Compound()
							attrib["Name"] = TAG_String(attribname)
							attrib["Base"] = TAG_Double(baseval)
							entity["SpawnPotentials"][slot]["Properties"]["Attributes"].append(attrib)
					elif filltype == "Add or Edit Attribute Modifier (Mobs and Items)":
						if entity["SpawnPotentials"][slot]["Type"].value == "Item":
							if "Item" not in entity["SpawnPotentials"][slot]["Properties"]:
								continue
							if "tag" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
								entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"] = TAG_Compound()
							if "AttributeModifiers" not in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
								entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["AttributeModifiers"] = TAG_List()
							for a in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["AttributeModifiers"]:
								if a["AttributeName"].value == attribname:
									a["Amount"] = TAG_Double(modamount)
									a["Operation"] = TAG_Int(modop)
									break
							else:
								attrib = TAG_Compound()
								attrib["Name"] = TAG_String(modname)
								attrib["AttributeName"] = TAG_String(attribname)
								attrib["Amount"] = TAG_Double(modamount)
								attrib["Operation"] = TAG_Int(modop)
								if uuidgen == "Generate Random UUID":
									uuidval = uuid.uuid4()
									least = uuidval.int & 0xFFFFFFFFFFFFFFFF
									most = uuidval.int >> 64
									if least > 9223372036854775807:
										least = least - 18446744073709551616
									if most > 9223372036854775807:
										most = most - 18446744073709551616
								elif uuidgen == "Use UUID Least and Most":
									least = uuidleast
									most = uuidmost
								elif uuidgen == "Use UUID String":
									uuidval = uuid.UUID(uuidstr)
									least = uuidval.int & 0xFFFFFFFFFFFFFFFF
									most = uuidval.int >> 64
									if least > 9223372036854775807:
										least = least - 18446744073709551616
									if most > 9223372036854775807:
										most = most - 18446744073709551616
								attrib["UUIDLeast"] = TAG_Long(least)
								attrib["UUIDMost"] = TAG_Long(most)
								entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["AttributeModifiers"].append(attrib)
						else:
							if "Attributes" not in entity["SpawnPotentials"][slot]["Properties"]:
								continue
							for a in entity["SpawnPotentials"][slot]["Properties"]["Attributes"]:
								if a["Name"].value == attribname:
									if "Modifiers" not in a:
										a["Modifiers"] = TAG_List()
									for m in a["Modifiers"]:
										if m["Name"].value == modname and m["Operation"] == modop:
											m["Amount"] = TAG_Double(modamount)
											break
									else:
										mod = TAG_Compound()
										mod["Name"] = TAG_String(modname)
										mod["Amount"] = TAG_Double(modamount)
										mod["Operation"] = TAG_Int(modop)
										if uuidgen == "Generate Random UUID":
											uuidval = uuid.uuid4()
											least = uuidval.int & 0xFFFFFFFFFFFFFFFF
											most = uuidval.int >> 64
											if least > 9223372036854775807:
												least = least - 18446744073709551616
											if most > 9223372036854775807:
												most = most - 18446744073709551616
										elif uuidgen == "Use UUID Least and Most":
											least = uuidleast
											most = uuidmost
										elif uuidgen == "Use UUID String":
											uuidval = uuid.UUID(uuidstr)
											least = uuidval.int & 0xFFFFFFFFFFFFFFFF
											most = uuidval.int >> 64
											if least > 9223372036854775807:
												least = least - 18446744073709551616
											if most > 9223372036854775807:
												most = most - 18446744073709551616
										mod["UUIDLeast"] = TAG_Long(least)
										mod["UUIDMost"] = TAG_Long(most)
										a["Modifiers"].append(mod)
					elif filltype == "List Attributes in Console":
						if "Attributes" in entity["SpawnPotentials"][slot]["Properties"]:
							print "Attributes for",entity["SpawnPotentials"][slot]["Type"].value,"in Slot",slot+1,"of spawner at",x,y,z,":"
							for a in entity["SpawnPotentials"][slot]["Properties"]["Attributes"]:
								print "Attribute:",a["Name"].value,", base:",str(a["Base"].value)
								if "Modifiers" in a:
									for m in a["Modifiers"]:
										print "Modifier:",m["Name"].value,", amount:",str(m["Amount"].value),", operation:",str(m["Operation"].value),","
										print "uuid:",uuid.UUID(int=(((m["UUIDMost"].value & 0xFFFFFFFFFFFFFFFF) << 64) | (m["UUIDLeast"].value& 0xFFFFFFFFFFFFFFFF))).hex
						elif "Item" in entity["SpawnPotentials"][slot]["Properties"]:
							if "tag" in entity["SpawnPotentials"][slot]["Properties"]["Item"]:
								if "AttributeModifiers" in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]:
									print "Attribute Modifiers for Item entity in Slot",slot+1,"of spawner at",x,y,z,":"
									for m in entity["SpawnPotentials"][slot]["Properties"]["Item"]["tag"]["AttributeModifiers"]:
										print "Attribute Modifier:",m["Name"].value,", amount:",str(m["Amount"].value),", operation:",str(m["Operation"].value),","
										print "uuid:",uuid.UUID(int=(((m["UUIDMost"].value & 0xFFFFFFFFFFFFFFFF) << 64) | (m["UUIDLeast"].value& 0xFFFFFFFFFFFFFFFF))).hex
					elif filltype == "Output SpawnPotentials Slot Properties to Console":
						print entity["SpawnPotentials"][slot]
					elif filltype == "Output Spawner Properties to Console":
						print entity
				if filltype != "Set SpawnPotentials Slot as Active Spawn":
					if not lockspawn:
						if "SpawnPotentials" in entity:
							if len(entity["SpawnPotentials"][0]) >= 1:
								if "Properties" in entity["SpawnPotentials"][0]:
									entity["SpawnData"] = deepcopy(entity["SpawnPotentials"][0]["Properties"])
									entity["EntityId"] = TAG_String(entity["SpawnPotentials"][0]["Type"].value)
				chunk.dirty = True


	if filltype == "Random Fill Number" or filltype == "Random Fill Percent":
		numblocks = int((box.maxy-box.miny)*(box.maxx-box.minx)*(box.maxz-box.minz))
		if filltype == "Random Fill Percent":
				count = int((box.maxy-box.miny)*(box.maxx-box.minx)*(box.maxz-box.minz) * (percentage*.01))
		itr = 0
		while itr < (count if count <= numblocks else numblocks) and itr < numblocks:
			numtries = 0
			while True:
				y = randrange(box.miny,box.maxy,1)
				x = randrange(box.minx,box.maxx,1)
				z = randrange(box.minz,box.maxz,1)
				if (x,y,z) not in randnumlist:
					randnumlist.append((x,y,z))
					break
				else:
					numtries = numtries + 1
					if numtries > numblocks:
						itr = numblocks
						break
			if not doreplace:
				if level.tileEntityAt(x,y,z):
					entitiesToRemove.append((level.getChunk(x>>4,z>>4),level.tileEntityAt(x,y,z)))
				SetBlock(x,y,z,True)
				itr = itr + 1
			elif doreplace and not donotreplace and level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData:
				if level.tileEntityAt(x,y,z):
					entitiesToRemove.append((level.getChunk(x>>4,z>>4),level.tileEntityAt(x,y,z)))
				SetBlock(x,y,z,True)
				itr = itr + 1
			elif donotreplace and not (level.blockAt(x, y, z) == blockreplace.ID and level.blockDataAt(x, y, z) == blockreplace.blockData):
				if level.tileEntityAt(x,y,z):
					entitiesToRemove.append((level.getChunk(x>>4,z>>4),level.tileEntityAt(x,y,z)))
				SetBlock(x,y,z,True)
				itr = itr + 1
		for (chunk, _, _) in level.getChunkSlices(box):
			(cx,cz) = chunk.chunkPosition
			cposx = cx * 16
			cposz = cz * 16
			for entity in addEntityList:
				if ((cposx <= entity["x"].value < (cposx + 16)) and (cposz <= entity["z"].value < (cposz + 16))):
					if spawntype:
						chunk.TileEntities.append(entity)
					else:
						chunk.Entities.append(entity)
		level.markDirtyBox(box)
	if "Fill" in filltype or filltype == "Spawner -> Spawner Minecart" or filltype == "Spawner Minecart -> Spawner" or filltype == "Entity -> Spawner":
		for (chunk, entity) in entitiesToRemove:
			if spawntype or filltype == "Spawner -> Spawner Minecart":
				chunk.TileEntities.remove(entity)
				chunk.dirty = True
			elif not spawntype or filltype == "Spawner Minecart -> Spawner" or filltype == "Entity -> Spawner":
				chunk.Entities.remove(entity)
				chunk.dirty = True
