# FoxelMap

FoxelMap is a (as of now crude) python command-line offline VoxelMap renderer that attempts to provide a customizable offline option for rendering voxelmap cache files, as well as adding extra modes and settings:

![example](debug_render_tile.png)

As of now it supports most but not all blockstates (namely waterlogged blocks). It also does not match voxelmap output 1:1 (and likely never will).

## Usage

Copy the 1.16 Minecraft `.jar` assets directory into the root folder of FoxelMap and copy the VoxelMap cache files of the world and dimension you wish to render into the `world/` folder.

To render the center regions of the world do `python foxelmap.py -x "-1,0" -z "-1,0" --stitch`, the output should then appear in `out/`!

### Modes
* **Terrain** - Voxelmap-like terrain output
* **Biome** - Biome colors using Amidst colors
* **Light** - Block Light of the main layer
* **Height** - Simple grayscale heightmap
* **Land** - Blank land and Water map

### Settings
* **Layer** - Ouput a single voxelmap layer
