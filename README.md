This repo acts an archive of the work of TexelElf - a former member of the minecraft map-making scene. Here you can find a collection of his mcedit-unified filters that were found previously on his [personal website](https://web.archive.org/web/20200628215159/http://elemanser.com/filters.html).

Do note that this repo acts strictly in the interest of preservation - maintenance, issues, and pull-requests will not be provided and/or accepted outside of its intended use case.

The following is a recreation of the TexelElf's filter homepage with updated links to filters and mentioned creators.

---

**Please note that these filters are at least two years old, and that nothing on this page is maintained any longer.**

This is a list of my MCEdit filters. Please note that I block adfly links; I do not allow people to profit directly off of my filters. Use these filters however you want, but please give credit if you modify or use pieces of one somewhere else. There are otherwise no restrictions on the usage of these filters. I can be contacted on [Twitter](http://twitter.com/TexelElf). I also showcase some of these filters on [my YouTube Channel](http://www.youtube.com/TexelElf)

---

MCEdit - The Minecraft Editor
- [MCEdit Unified](https://podshot.github.io/MCEdit-Unified/) is the recommended MCEdit version for the majority of filters on this page
- [MCEdit Unified Dev builds](https://github.com/Podshot/MCEdit-Unified-Preview/releases) are experimental builds that add newer functionality; use at your own risk!
- [MCEdit 2.0](https://www.mcedit.net/) is the next generation of MCEdit in development by the original MCEdit author codewarri0r. None of the filters on this page work in this version.

---

Other MCEdit filter authors:
- [Adrian Brightmoore](https://github.com/abrightmoore/ScriptsForMCEdit)
- [SethBling](https://sethbling.s3.us-west-2.amazonaws.com/Downloads/Filters/index.html)
- [gentlegiantJGC](https://github.com/gentlegiantJGC/MCEdit-Filters)

**Command Block Filters:**
- [Absolute To Relative](filters/AbsToRel.py) converts absolute coordinates to relative and vice versa; it can also move (offset) coordinates.
- [ToBlockCommand](filters/ToBlockCommand.py) can create setblock, summon, clone, fill, testforblock, blockdata, and testforblocks commands.
- [ToSummonCommand](filters/ToSummonCommand.py) will create a summon command for each entity inside of the selection.
- [Chest Contents To Command](filters/ChestContentsToCommand.py) converts a chest into a give or summon command, depending on the number of items in the chest.
- [Edit Command Block](filters/EditControl.py) allows you to create and edit command blocks. It can create newlines and section characters, do simple and regex string replaces, and more.
- [Pinata](filters/Pinata.py) turns a chest into a trio of commands that dump the chest's contents over an area along with a firework flourish.
- [Command Block To Minecart](filters/CommandBlockToMinecart.py) turns a Command Block into a MinecartCommandBlock and vice versa.
- [Dump Command Blocks](filters/DumpCommandBlocks.py) will dump a selection's command blocks into an editable text file that can later be re-imported using this filter.
- [Fix Lag](filters/FixLag.py) "fixes" lag by deleting the "LastOutput" tag and setting "TrackOutput" to false on all selected command blocks.

**All-Purpose Filters:**
- [NBT Editor Filter (Windows Version)](filters/NBT.zip) can edit the NBT of selected entities, tile entities, and tile ticks. It can also edit NBT-formatted DAT files and schematics.
- [NBT Editor Filter (Multiplatform Version)](filters/NBT_Multi.py) same as above, except this will work on Macintosh and Linux platforms. On Linux platforms, ensure that python-tk is installed.
- [NBT Editor Filter (Bedrock/PE, Windows Only)](https://github.com/gentlegiantJGC/MCEdit-Filters/tree/master/Bedrock%20Edition%20Filters) is a version of the above filter maintained by gentlegiantJGC that works with Bedrock (Windows 10 and PE) versions of Minecraft. Please note you'll need to use the development version of MCEdit for this to work.
- [Apply Block Lighting](filters/ApplyBlockLighting.py) changes the default luminosity and opacity that MCEdit uses during its lighting operations. You can also unmark chunks for relighting using this filter.
- [Ron Smalec's Chest Filter](filters/RSmalecChestFilter.py) allows the editing of containers in a very wide variety of ways, using a variety of search criteria.
- [Find](filters/Find.py) will find blocks by block ID/NBT data, and entities/tile entities by NBT data; it will move the camera to found objects. It will do a recursive search though the tags.

**Specialty Filters:**
- [MapIt](filters/MapIt.py) converts images into Minecraft maps mounted in item frames. Ensure that you are using the latest version of MCEdit Unified, otherwise you may get errors.
- [MapIt for Minecraft Windows 10 (Bedrock)/PE](https://github.com/gentlegiantJGC/MCEdit-Filters/tree/master/Bedrock%20Edition%20Filters) is another gentlegiantJGC-maintained filter that updates the original MapIt filter, allowing users to import images into Minecraft Windows 10/Bedrock/PE versions. This filter only works with the development version of MCEdit.
- [Batch MapIt](filters/BatchIt.py) is similar to the ordinary version of MapIt, but will process an entire folder of images. It will not create chests or item frames; it does create a CSV file in the data directory with map IDs.
- [Dump Commands](filters/DumpCommands.py) will dump the commands in every command block into a text file; it does no importing.
- [Lighting Bug](filters/LightingBug.py) will set the world's height map to the lowest portion of the selection and will also set the block light level.
- [Ani's Invulnerability Filter](filters/AniInvulnerability.py) sets the "Invulnerable" tag on any entity within the selection.
- [Tomutwit's Giant Filter](filters/TomutwitMakeGiant.py) sets an entity's "id" tag to "Giant." It can also apply persistence.
- [Nirgalbunny's Beacon Filter](filters/NirgaleseBeaconFilter.py) lets you set the active effect a beacon is emitting.
- [TileTick Filter](filters/TileTickFilter.py) creates tile ticks (block updates).
- [Vladimyr's Locksmith Filter](filters/VladLocksmith.py) creates lock hoppers.
- [Head Filter](filters/HeadFilter.py) used to place player heads as blocks or as items on mobs.


**Block Editing Filters:**
- [Jigarbov's Block Filter](filters/JigarbovBlockFilter.py) allows you to replace target blocks with source other blocks, and at weighted rates. It can also ignore block data (e.g., a torch's direction).
- [Q-magnet's Scaler](filters/QScale.py) performs a simple scaling operation of the selection, with individual scale ratios allowed per each axis.
- [Block Liner](filters/BlockLiner.py) will line a shape with blocks depending on the faces and shape specified.
- [Make Shapes](filters/MakeShapes.py) is an incomplete shape creator. It can make ellipsoids and cylinders.


**Crap made for TrazLander or Moesh:**
- [commandblocksigns+](filters/commandblocksigns+.py) is an edit of one of SethBling's filters.
- [Moesh's Chunk Loader](filters/MoeshChunks.py) creates a sequence of commands that can keep chunks loaded.
- [TrazLander's Chest Filter](filters/TrazChestFilter.py) is an early and crappy version of Ron Smalec's Chest Filter, located above.
- [TrazLander's Spawner Filter](filters/TrazSpawnerFilter.py) is an obsolete filter that used signs to create redstone-activated spawners or command blocks for summoning entities.
- [TrazLander's Command Filter](filters/TrazCommandFilter.py) an untested version of the above filter specifically designed for creating command blocks.
- [TrazLander's Swapper Filter](filters/TrazSwapperFilter.py) is an obsolete filter that automated the creation of block-swapping redstone-activated spawners. It can also create summon commands.
- [Replace Command Blocks](filters/ReplaceCommandBlocks.py) replaces matching command blocks with a specified block.


**Mob Spawner Filters:**
- [Unified Spawner Filter](filters/UnifiedSpawnerFilter.py) can create spawners of just about anything.
- [Complete Mob Equipment Filter](filters/EquipmentFilter.py) lets you set the equipment on mobs inside of a spawner.
- [Change Range](filters/ChangeRange.py) allows you to set the various initial parameters of a mob spawner; the spawn rate, count, detection radius, etc.
- [Offset Spawners](filters/OffsetSpawners.py) moves the spawn location of spawners.


**Junk Drawer:** (miscellaneous junk filters. Often half-completed or obsolete filters made for fixing various things Mojang broke)

- [AMLP's Secret Block Filter](filters/AMLPSecretBlock.py) is a block "36-ifier" filter. It creates block 36 along with an associated piston tile entity.
- [De-36ify](filters/de-36ify.py) will undo the above filter; it was made before you could disable the Undo feature in MCEdit.
- [ToCloneCommand](filters/ToCloneCommand.py) is an early version of ToBlockCommand that can only make clone commands.
- [Snapatya's Block Rotator](filters/SnapatyaBlockRotator.py), made at some random dude's request, can rotate faced blocks (e.g., furnaces, chests, etc.).
- [TileEntity To Command](filters/TileEntityToCommand.py) is another early, obsolete version of ToBlockCommand; this one will convert a spawner into a summon command, however.
- [Place Blocks](filters/PlaceBlocks.py) is yet another obsolete precursor to ToBlockCommand.
- [Repair Chunk Entities](filters/RepairChunkEntities.py) tries to remove entities stored in the wrong chunks and place them in the correct chunks.
- [Light Redstone](filters/LightRedstone.py) attempts to place glowstone next to repeaters and the like.
- [Fix FallingSand](filters/FixFallingSand.py) fixes the Time and/or Block tags of FallingSand spawners. Useful if your spawners are spawning sand and not other block types.
- [Fix Shops](filters/FixShops.py) changes the broken block 36 trade in villagers.
- [Fix Health](filters/FixHealth.py) "fixed" Health and HealF tags.
- [Mirror Sign Posts](filters/MirrorSignPosts.py) is self-explanatory.
- [Set Selection](filters/SelSet.py) sets the selection and moves the camera. Mostly a proof-of-concept filter.
- [Attribute Filter](filters/AttributeFilter.py) sets entity attributes.
- [Summon To SetBlock](filters/SummonToSetBlock.py) would convert summon commands to setblock commands; made when setblock was first introduced.
- [Drippy Noise](filters/DrippyNoise.py) is a half-completed noise filter I created for Jigarbov.
- [Jigarbov's Control Filter](filters/JigarbovControlFilter.py) does something with coordinates for tp commands, I think. I made it at his request.
- [Jigarbov's Multiplex Filter](filters/Multiplex.py) was created by request to help export regions with deeply nested mob spawners and other things that MCEdit can't handle by default. Used in Adventure Multiplex 2.
- [ID Converter](filters/OmoIDConverter.py) will convert old numeric IDs to the new ones for containers.
- [Stack Spawner Carts](filters/StackSpawnerCarts.py) will move all spawner carts within the selection to the same location.
- [Set Enchant and Color](filters/SetEnchantAndColor.py) is an early component to the Complete Mob Equipment Filter above.
- [Set Equipment](filters/SetEquipment.py) is an early component to the Complete Mob Equipment Filter above.
- [Xisuma Void's Minecart Filter](filters/XisumaCartFilter.py) creates minecarts with the DisplayBlock set.
- [Vexian Spawner Filter](filters/VexianSpawnerCreator.py) a precursor to the Unified Spawning Filter, this filter specialized in creating non-mob spawners.
- [Mob Spawner Fill](filters/MobSpawnerFill.py) my very first filter, and a precursor to the Unified Spawning Filter, this filter was a modification of a SethBling filter that specializes in creating mob spawners.