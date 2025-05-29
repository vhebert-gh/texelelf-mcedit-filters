from copy import deepcopy
displayName = "Apply Block Lighting"

block_lights = {
	"minecraft:air":0,"minecraft:stone":0,"minecraft:grass":0,"minecraft:dirt":0,"minecraft:cobblestone":0,"minecraft:planks":0,"minecraft:sapling":0,
	"minecraft:bedrock":0,"minecraft:flowing_water":0,"minecraft:water":0,"minecraft:flowing_lava":15,"minecraft:lava":15,"minecraft:sand":0,"minecraft:gravel":0,
	"minecraft:gold_ore":0,"minecraft:iron_ore":0,"minecraft:coal_ore":0,"minecraft:log":0,"minecraft:leaves":0,"minecraft:sponge":0,"minecraft:glass":0,
	"minecraft:lapis_ore":0,"minecraft:lapis_block":0,"minecraft:dispenser":0,"minecraft:sandstone":0,"minecraft:noteblock":0,"minecraft:bed":0,"minecraft:golden_rail":0,
	"minecraft:detector_rail":0,"minecraft:sticky_piston":0,"minecraft:web":0,"minecraft:tallgrass":0,"minecraft:deadbush":0,"minecraft:piston":0,
	"minecraft:piston_head":0,"minecraft:wool":0,"minecraft:piston_extension":0,"minecraft:yellow_flower":0,"minecraft:red_flower":0,"minecraft:brown_mushroom":1,
	"minecraft:red_mushroom":0,"minecraft:gold_block":0,"minecraft:iron_block":0,"minecraft:double_stone_slab":0,"minecraft:stone_slab":0,"minecraft:brick_block":0,
	"minecraft:tnt":0,"minecraft:bookshelf":0,"minecraft:mossy_cobblestone":0,"minecraft:obsidian":0,"minecraft:torch":14,"minecraft:fire":15,"minecraft:mob_spawner":0,
	"minecraft:oak_stairs":0,"minecraft:chest":0,"minecraft:redstone_wire":0,"minecraft:diamond_ore":0,"minecraft:diamond_block":0,"minecraft:crafting_table":0,
	"minecraft:wheat":0,"minecraft:farmland":0,"minecraft:furnace":0,"minecraft:lit_furnace":13,"minecraft:standing_sign":0,"minecraft:wooden_door":0,
	"minecraft:ladder":0,"minecraft:rail":0,"minecraft:stone_stairs":0,"minecraft:wall_sign":0,"minecraft:lever":0,"minecraft:stone_pressure_plate":0,
	"minecraft:iron_door":0,"minecraft:wooden_pressure_plate":0,"minecraft:redstone_ore":0,"minecraft:lit_redstone_ore":9,"minecraft:unlit_redstone_torch":0,
	"minecraft:redstone_torch":7,"minecraft:stone_button":0,"minecraft:snow_layer":0,"minecraft:ice":0,"minecraft:snow":0,"minecraft:cactus":0,"minecraft:clay":0,
	"minecraft:reeds":0,"minecraft:jukebox":0,"minecraft:fence":0,"minecraft:pumpkin":0,"minecraft:netherrack":0,"minecraft:soul_sand":0,"minecraft:glowstone":15,
	"minecraft:portal":11,"minecraft:lit_pumpkin":15,"minecraft:cake":0,"minecraft:unpowered_repeater":0,"minecraft:powered_repeater":0,"minecraft:stained_glass":0,
	"minecraft:trapdoor":0,"minecraft:monster_egg":0,"minecraft:stonebrick":0,"minecraft:brown_mushroom_block":0,"minecraft:red_mushroom_block":0,
	"minecraft:iron_bars":0,"minecraft:glass_pane":0,"minecraft:melon_block":0,"minecraft:pumpkin_stem":0,"minecraft:melon_stem":0,"minecraft:vine":0,
	"minecraft:fence_gate":0,"minecraft:brick_stairs":0,"minecraft:stone_brick_stairs":0,"minecraft:mycelium":0,"minecraft:waterlily":0,"minecraft:nether_brick":0,
	"minecraft:nether_brick_fence":0,"minecraft:nether_brick_stairs":0,"minecraft:nether_wart":0,"minecraft:enchanting_table":0,"minecraft:brewing_stand":1,
	"minecraft:cauldron":0,"minecraft:end_portal":15,"minecraft:end_portal_frame":1,"minecraft:end_stone":0,"minecraft:dragon_egg":1,"minecraft:redstone_lamp":0,
	"minecraft:lit_redstone_lamp":15,"minecraft:double_wooden_slab":0,"minecraft:wooden_slab":0,"minecraft:cocoa":0,"minecraft:sandstone_stairs":0,
	"minecraft:emerald_ore":0,"minecraft:ender_chest":7,"minecraft:tripwire_hook":0,"minecraft:tripwire":0,"minecraft:emerald_block":0,"minecraft:spruce_stairs":0,
	"minecraft:birch_stairs":0,"minecraft:jungle_stairs":0,"minecraft:command_block":0,"minecraft:beacon":15,"minecraft:cobblestone_wall":0,"minecraft:flower_pot":0,
	"minecraft:carrots":0,"minecraft:potatoes":0,"minecraft:wooden_button":0,"minecraft:skull":0,"minecraft:anvil":0,"minecraft:trapped_chest":0,
	"minecraft:light_weighted_pressure_plate":0,"minecraft:heavy_weighted_pressure_plate":0,"minecraft:unpowered_comparator":0,"minecraft:powered_comparator":0,
	"minecraft:daylight_detector":0,"minecraft:redstone_block":0,"minecraft:quartz_ore":0,"minecraft:hopper":0,"minecraft:quartz_block":0,"minecraft:quartz_stairs":0,
	"minecraft:activator_rail":0,"minecraft:dropper":0,"minecraft:stained_hardened_clay":0,"minecraft:stained_glass_pane":0,"minecraft:leaves2":0,"minecraft:log2":0,
	"minecraft:acacia_stairs":0,"minecraft:dark_oak_stairs":0,"minecraft:slime":0,"minecraft:barrier":0,"minecraft:iron_trapdoor":0,"minecraft:prismarine":0,
	"minecraft:sea_lantern":15,"minecraft:hay_block":0,"minecraft:carpet":0,"minecraft:hardened_clay":0,"minecraft:coal_block":0,"minecraft:packed_ice":0,
	"minecraft:double_plant":0
	}

block_opacity = {
	"minecraft:air":0,"minecraft:stone":15,"minecraft:grass":15,"minecraft:dirt":15,"minecraft:cobblestone":15,"minecraft:planks":15,"minecraft:sapling":0,
	"minecraft:bedrock":15,"minecraft:flowing_water":3,"minecraft:water":3,"minecraft:flowing_lava":15,"minecraft:lava":15,"minecraft:sand":15,"minecraft:gravel":15,
	"minecraft:gold_ore":15,"minecraft:iron_ore":15,"minecraft:coal_ore":15,"minecraft:log":15,"minecraft:leaves":1,"minecraft:sponge":15,"minecraft:glass":0,
	"minecraft:lapis_ore":15,"minecraft:lapis_block":15,"minecraft:dispenser":15,"minecraft:sandstone":15,"minecraft:noteblock":15,"minecraft:bed":0,"minecraft:golden_rail":0,
	"minecraft:detector_rail":0,"minecraft:sticky_piston":0,"minecraft:web":1,"minecraft:tallgrass":0,"minecraft:deadbush":0,"minecraft:piston":0,
	"minecraft:piston_head":0,"minecraft:wool":15,"minecraft:piston_extension":15,"minecraft:yellow_flower":0,"minecraft:red_flower":0,"minecraft:brown_mushroom":0,
	"minecraft:red_mushroom":0,"minecraft:gold_block":15,"minecraft:iron_block":15,"minecraft:double_stone_slab":15,"minecraft:stone_slab":15,"minecraft:brick_block":15,
	"minecraft:tnt":15,"minecraft:bookshelf":15,"minecraft:mossy_cobblestone":15,"minecraft:obsidian":15,"minecraft:torch":0,"minecraft:fire":0,"minecraft:mob_spawner":0,
	"minecraft:oak_stairs":15,"minecraft:chest":0,"minecraft:redstone_wire":0,"minecraft:diamond_ore":15,"minecraft:diamond_block":15,"minecraft:crafting_table":15,
	"minecraft:wheat":0,"minecraft:farmland":15,"minecraft:furnace":15,"minecraft:lit_furnace":13,"minecraft:standing_sign":0,"minecraft:wooden_door":0,
	"minecraft:ladder":0,"minecraft:rail":0,"minecraft:stone_stairs":15,"minecraft:wall_sign":0,"minecraft:lever":0,"minecraft:stone_pressure_plate":0,
	"minecraft:iron_door":0,"minecraft:wooden_pressure_plate":0,"minecraft:redstone_ore":15,"minecraft:lit_redstone_ore":9,"minecraft:unlit_redstone_torch":0,
	"minecraft:redstone_torch":0,"minecraft:stone_button":0,"minecraft:snow_layer":0,"minecraft:ice":3,"minecraft:snow":15,"minecraft:cactus":0,"minecraft:clay":15,
	"minecraft:reeds":0,"minecraft:jukebox":15,"minecraft:fence":0,"minecraft:pumpkin":15,"minecraft:netherrack":15,"minecraft:soul_sand":15,"minecraft:glowstone":15,
	"minecraft:portal":0,"minecraft:lit_pumpkin":15,"minecraft:cake":0,"minecraft:unpowered_repeater":0,"minecraft:powered_repeater":0,"minecraft:stained_glass":0,
	"minecraft:trapdoor":0,"minecraft:monster_egg":15,"minecraft:stonebrick":15,"minecraft:brown_mushroom_block":15,"minecraft:red_mushroom_block":15,
	"minecraft:iron_bars":0,"minecraft:glass_pane":0,"minecraft:melon_block":15,"minecraft:pumpkin_stem":0,"minecraft:melon_stem":0,"minecraft:vine":0,
	"minecraft:fence_gate":0,"minecraft:brick_stairs":15,"minecraft:stone_brick_stairs":15,"minecraft:mycelium":15,"minecraft:waterlily":0,"minecraft:nether_brick":15,
	"minecraft:nether_brick_fence":0,"minecraft:nether_brick_stairs":15,"minecraft:nether_wart":0,"minecraft:enchanting_table":0,"minecraft:brewing_stand":0,
	"minecraft:cauldron":0,"minecraft:end_portal":0,"minecraft:end_portal_frame":0,"minecraft:end_stone":15,"minecraft:dragon_egg":0,"minecraft:redstone_lamp":15,
	"minecraft:lit_redstone_lamp":15,"minecraft:double_wooden_slab":15,"minecraft:wooden_slab":15,"minecraft:cocoa":0,"minecraft:sandstone_stairs":15,
	"minecraft:emerald_ore":15,"minecraft:ender_chest":0,"minecraft:tripwire_hook":0,"minecraft:tripwire":0,"minecraft:emerald_block":15,"minecraft:spruce_stairs":15,
	"minecraft:birch_stairs":15,"minecraft:jungle_stairs":15,"minecraft:command_block":15,"minecraft:beacon":0,"minecraft:cobblestone_wall":0,"minecraft:flower_pot":0,
	"minecraft:carrots":0,"minecraft:potatoes":0,"minecraft:wooden_button":0,"minecraft:skull":0,"minecraft:anvil":0,"minecraft:trapped_chest":0,
	"minecraft:light_weighted_pressure_plate":0,"minecraft:heavy_weighted_pressure_plate":0,"minecraft:unpowered_comparator":0,"minecraft:powered_comparator":0,
	"minecraft:daylight_detector":0,"minecraft:redstone_block":15,"minecraft:quartz_ore":15,"minecraft:hopper":0,"minecraft:quartz_block":15,"minecraft:quartz_stairs":15,
	"minecraft:activator_rail":0,"minecraft:dropper":0,"minecraft:stained_hardened_clay":15,"minecraft:stained_glass_pane":0,"minecraft:leaves2":1,"minecraft:log2":15,
	"minecraft:acacia_stairs":15,"minecraft:dark_oak_stairs":15,"minecraft:slime":15,"minecraft:barrier":0,"minecraft:iron_trapdoor":0,"minecraft:prismarine":15,
	"minecraft:sea_lantern":15,"minecraft:hay_block":15,"minecraft:carpet":0,"minecraft:hardened_clay":15,"minecraft:coal_block":15,"minecraft:packed_ice":15,
	"minecraft:double_plant":0
	}

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
	160:"minecraft:stained_glass_pane",161:"minecraft:leaves2",162:"minecraft:log2",163:"minecraft:acacia_stairs",164:"minecraft:dark_oak_stairs",165:"minecraft:slime",
	166:"minecraft:barrier",167:"minecraft:iron_trapdoor",168:"minecraft:prismarine",169:"minecraft:sea_lantern",170:"minecraft:hay_block",171:"minecraft:carpet",
	172:"minecraft:hardened_clay",173:"minecraft:coal_block",174:"minecraft:packed_ice",175:"minecraft:double_plant"
}

inputs = (
	("It is recommended that you modify lighting as the last step in editing your world.  You must save the world for MCEdit to update the lighting using the values you've specified.","label"),
	("Lighting operation:",("Custom + Default","Custom Only","Reset to Default","Blacken","Brighten","Twilight","Unmark chunks for relighting")),
	("Enter custom block lighting in a comma-separated list using the full block name and the lighting level between 0 and 15.\n"
		"E.g.:\nminecraft:stone=15,minecraft:dirt=3","label"),
	("Custom Block Lighting:",("string","value=None","width=700")),
	("Comma-separated list of a block's opacity. 0 is transparent, 15 is completely opaque.","label"),
	("Custom Block Opacity:",("string","value=None","width=700")),
	("Apply to whole chunk (if unchecked, you must update the block in-game for the lighting to change):",True),
	)


def perform(level, box, options):
	op = options["Lighting operation:"]
	wholechunk = options["Apply to whole chunk (if unchecked, you must update the block in-game for the lighting to change):"]
	block_lights_copy = deepcopy(block_lights)
	block_opacity_copy = deepcopy(block_opacity)

	if "Default" in op:
		for a in block_map.keys():
			level.materials.lightEmission[a] = block_lights_copy[block_map[a]]
			level.materials.lightAbsorption[a] = block_opacity_copy[block_map[a]]
	if op == "Blacken" or op == "Custom Only":
		for a in range(len(level.materials.lightEmission)):
			level.materials.lightEmission[a] = 0
			level.materials.lightAbsorption[a] = 15
			if a in block_map:
				block_lights_copy[block_map[a]] = 0
	elif op == "Brighten":
		for a in range(len(level.materials.lightEmission)):
			level.materials.lightEmission[a] = 15
			level.materials.lightAbsorption[a] = 0
			if a in block_map:
				block_lights_copy[block_map[a]] = 15
	elif op == "Twilight":
		for a in range(len(level.materials.lightEmission)):
			level.materials.lightEmission[a] = 7
			level.materials.lightAbsorption[a] = 7
			if a in block_map:
				block_lights_copy[block_map[a]] = 7
	if "Custom" in op:
		if options["Custom Block Lighting:"] and options["Custom Block Lighting:"].upper() != "NONE":
			try:
				for a in options["Custom Block Lighting:"].split(","):
					b = a.split("=")
					newlight = int(b[1])
					if newlight < 0:
						newlight = 0
					elif newlight > 15:
						newlight = 15
					block_lights_copy[b[0]] = newlight
			except:
				raise Exception("Error parsing Custom Block Lighting. Please verify your syntax, that the block name is correct, or that the block exists in the filter's block arrays.")
		if options["Custom Block Opacity:"] and options["Custom Block Opacity:"].upper() != "NONE":
			try:
				for a in options["Custom Block Opacity:"].split(","):
					b = a.split("=")
					newlight = int(b[1])
					if newlight < 0:
						newlight = 0
					elif newlight > 15:
						newlight = 15
					block_opacity_copy[b[0]] = newlight
			except:
				raise Exception("Error parsing Custom Block Opacity. Please verify your syntax, that the block name is correct, or that the block exists in the filter's block arrays.")
		for a in block_map.keys():
			level.materials.lightEmission[a] = block_lights_copy[block_map[a]]
			level.materials.lightAbsorption[a] = block_opacity_copy[block_map[a]]


	for (chunk, _, _) in level.getChunkSlices(box):
		if op == "Unmark chunks for relighting":
			chunk.needsLighting = False
		elif wholechunk:
			chunk.dirty = True
			chunk.needsLighting = True
		else:
			(cx,cz) = chunk.chunkPosition
			cposx = cx * 16
			cposz = cz * 16
			for y in xrange(box.miny,box.maxy,1):
				for z in xrange(max(cposz, box.minz),min(cposz+16, box.maxz),1):
					for x in xrange(max(cposx, box.minx),min(cposx+16, box.maxx),1):
						chx = x-cposx
						chz = z-cposz
						block = chunk.Blocks[chx,chz,y]
						newlight = 0
						if block in block_map:
							if block_map[block] in block_lights_copy:
								newlight = block_lights_copy[block_map[block]]
						chunk.BlockLight[chx,chz,y] = newlight
						chunk.dirty = True
						chunk.needsLighting = False
						