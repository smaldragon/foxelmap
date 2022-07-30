# FoxelMap

FoxelMap is a (as of now crude) python command-line offline 1.16.5 to 1.19 VoxelMap renderer that attempts to provide a customizable offline option for rendering voxelmap cache files, as well as adding extra modes and settings:

![example](debug_render_tile.png)

As of now it supports most but not all blockstates (namely waterlogged blocks). It also does not match voxelmap output 1:1 (and likely never will).

## Usage

**FoxelMap 0.1** - Back from Hiatus

Copy the VoxelMap cache `.zip` files of the world and dimension you wish to render into a new folder named `world`inside the Foxelmap directory

To render the center regions of your world do `python foxelmap.py --radius 3 --stitch`, the output should then appear in `out/`!

Run `python foxelmap.py --help` for a list of all commands and settings or view the tables bellow.

### Setup

Commands that will be run most times

| Command            | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `--world <path>`   | The path to the folder with the .zip tiles to be rendered, `world/` is the default if no world setting is specified |
| `--v <16/17/18/19>`   | The Minecraft version this data belongs to, supported values are `16, 17, 18 or 19` |

### Area Selection

Voxelmap stores its cache data in tiles each corresponding to a 256x256 area (as opposed to the 512x512 of minecraft's region files). Several commands are available for picking which tiles to render with Foxelmap.

| Command            | Description                                                  |
| ------------------ | ------------------------------------------------------------ |
| `-a` / `--all`     | Render all tiles in the cache                                |
| `-c "x,z"`         | Renders the tile at the specified x,z in-game coordinate     |
| `--cx "x1,x2"`     | Renders the tiles between the specified x in-game coordinates (inclusive) |
| `--cz "z1,z2"`     | Renders the tiles between the specified z in-game coordinates (inclusive) |
| `-t "x,z"`         | Renders the tile at the specified x,z voxelmap tile coordinate |
| `--tx "x1,x2"`     | Renders the tiles between the specified x voxelmap tile coordinates (inclusive) |
| `--tz "x1,x2"`     | Renders the tiles between the specified z voxelmap tile coordinates (inclusive) |
| `--radius <value>` | Expands the selected tile area by a specified radius in all directions |

### Render Modes

| Command          | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| `--mode terrain` | The standard Voxelmap-like look                              |
| `--mode height`  | A grayscale map where pixel brightness = y                   |
| `--mode light`   | À grayscale map showing the block light level                |
| `--mode land`    | A map showing the water and land boundaries                  |
| `--mode biome`   | A map of the different biomes using Amidst color values      |
| `--mode none`    | Performs no render. Stitch, zoom and atlas commands continue to work as usual |

#### Render Settings

| Command                                | Description                                                  |
| -------------------------------------- | ------------------------------------------------------------ |
| `--light <day/night/nether/end/gamma>` | When in `--mode terrain`, selects the lighting to use for rendering |
| `--bedrock`                            | When in `--mode terrain`, uses minecraft bedrock edition water colors |
| `--noyshading`                         | When in `--mode terrain`, disables tinting blocks according to y level |
| `--heightslice <value>`                | When in `--mode height` rounds the values of y coordinates to intervals of the specified value to create a layered topographic look |
| `--layer`                              | In `terrain` and `height` modes, renders a single Voxelmap layer (0 = Surface, 1 = Underwater, 2 = Transparent Blocks, 3 = Vegetation) |

### Output Settings

| Command          | Description                                                  |
| ---------------- | ------------------------------------------------------------ |
| `--zoom <value>` | Creates folders with zoomed out versions of the tiles, every 4 tiles in a certain zoom level get merged and shrunk into a single 256x256 tile at the next zoom level |
| `--stitch`       | Stitches all the produced tiles into a single image, if zoom is used, it will use the highest zoom level |

### Atlas Settings

To generate its terrain map Foxelmap uses a pixel atlas with the colors to be used for each block, by default Foxelmap now comes with a pre-calculated atlas, however it is also possible to generate new ones. To do this, copy the 1.16 Minecraft `.jar` assets directory into the root folder of Foxelmap and run one of the following commands.

| Command      | Description                                                  |
| ------------ | ------------------------------------------------------------ |
| `--atlas`    | Uses the minecraft assets/ folder to generate block colors   |
| `--atlasgen` | Uses the minecraft assets/ folder to generate block colors and outputs them to file (note: this overwrites the default provided one) |

