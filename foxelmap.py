#!/usr/bin/python

import sys, getopt
import numpy_render
import atlas_gen
import stitch
import os
import math
import merger

try:
    os.makedirs('out/z0')
except:
    pass

# Features:
# Different rendering output modes: terrain, elevation and landmass (configurable sea level y)
# Time of day (plus end,nether and gamma)
# Render Biomes with Bedrock Colors

# Issues:
# Block states are partially supported (no waterlogging)

# Not pixel accurate to real Voxel Map (unsure if it ever will be) [very close now]
# Biome tints are currently hard-coded (using values from minecraft wiki)
# No mod support (sorry)
# No resource pack support
# Only supports latest voxelmap version/format (and only tested with minecraft 1.16.5)
# Block slopes breaks across region edges
# Different toggles for terrain/slope/water not yet avaliable
# Only supports/tested with the overworld dimension
# Add better help/documentation
# Send a single variable for atlases and modes

def main(argv):
    bounds_x = None
    bounds_z = None
    render_all = False
    stitch_tiles = False
    config = {}
    mode = "terrain"
    world = ["world"]
    time_of_day = "day"
    bedrock = False
    zoom = 0

    try: 
        opts, args = getopt.getopt(argv,"hx:z:am:w:c:",
            ["all","stitch","radius=","mode=","world=","light=","bedrock","help","cx=","cz=","zoom=","heightslice=","layer="]
        )
    except getopt.GetoptError:
        print("foxelmap.py -x \"x1,x2\" -z \"z1,z2\"")
        sys.exit(2)
    for opt,arg in opts:
        if opt in ('-h','--help'):
            print ("FoxelMap Renderer")
            print (".\\foxelmap.py -x \"-1,1\" -z \"-1,1\"")
            print("")
            print("\t-a --all - renders all tiles")
            print("\t-x \"x1,x2\" - region x")
            print("\t-z \"z1,z2\" - region z")
            print("\t-c \"x,z\" - tile at x,z ingame coords")
            print("\t--cx \"x1,x2\" - tiles from x1 to x2 ingame coords")
            print("\t--cz \"z1,z2\" - tiles from z1 to z2 ingame coords")
            print("")
            print("\t--mode <terrain|height|light|biome>")
            print("\t--light <day|night|nether|end|gamma>")
            print("\t--bedrock - use bedrock edition biome colors")
            print("\t--heightslice <slice> - thickness of layers in height mode")
            print("\t--layer <layer> | choose a single voxelmap layer to render")
            print("")
            print("\t--zoom z")
            print("\t--stitch - produces a single image file with all tiles")
            print("\n")
            sys.exit()
        elif opt in ("-x"):
            render_all = False
            split = arg.split(",")
            if len(split) == 1:
                bounds_x = [int(arg),int(arg)]
            if len(split) == 2:
                bounds_x = [int(split[0]),int(split[1])]
                bounds_x.sort()
        elif opt in ("-z"):
            render_all = False
            split = arg.split(",")
            if len(split) == 1:
                bounds_z = [int(arg),int(arg)]
            if len(split) == 2:
                bounds_z = [int(split[0]),int(split[1])]
                bounds_z.sort()
        elif opt in ("--radius"):
            if bounds_x == None: bounds_x = [0,0]
            if bounds_z == None: bounds_z = [0,0]
            bounds_x = [bounds_x[0] -int(arg),bounds_x[1] + int(arg)]
            bounds_z = [bounds_z[0] -int(arg),bounds_z[1] + int(arg)]
            
        elif opt in ("-a","--all"):
            render_all = True
        elif opt in ("--stitch"):
            stitch_tiles = True
        elif opt in ("-m","--mode"):
            if arg in ("terrain","land","biome","light","height","none"):
                mode = arg
        elif opt in ("-w","--world"):
            world = arg.split(",")
        elif opt in ("--light"):
            time_of_day = arg
        elif opt in ("-c"):
            split = arg.split(",")
            cx = math.floor(int(split[0])/256)
            cz = math.floor(int(split[1])/256)
            bounds_x = [cx,cx]
            bounds_z = [cz,cz]
        elif opt in ("--cx"):
            split = arg.split(",")
            cx1 = math.floor(int(split[0])/256)
            cx2 = math.floor(int(split[1])/256)
            bounds_x = [cx1,cx2]
            bounds_x.sort()
        elif opt in ("--cz"):
            split = arg.split(",")
            cz1 = math.floor(int(split[0])/256)
            cz2 = math.floor(int(split[1])/256)
            bounds_z = [cz1,cz2]
            bounds_z.sort()
        elif opt in ("--bedrock"):
            bedrock = True
        elif opt in ("--zoom"):
            zoom = int(arg)
        elif opt in ("--heightslice"):
            config['cut'] = int(arg)
        elif opt in ('--layer'):
            config['render_layer'] = int(arg)

    print(world)

    #if (bounds_x == None or bounds_z == None) and render_all == False:
    #    print("ERROR: Invalid Map Bounds")
    #    sys.exit(1)
    if (world == ""):
        print("ERROR: No World Provided")
        sys.exit(1)
    
    print(bounds_x,bounds_z)
    atlas = None
    light_atlas = None
    biome_atlas = None
    if mode == "terrain":
        atlas = atlas_gen.get_atlas(bedrock)
    if mode in ("terrain","light"):
        light_atlas = atlas_gen.get_light_atlas(time_of_day)
    if mode in ("terrain","biome"):
        biome_atlas = atlas_gen.get_biome_atlas()

    print("bounds is",bounds_x,bounds_z)
    for w in world:
        print("printing tiles for {}".format(w))
        if len(world) == 1:
            out = ""
        else:
            out = "{}/".format(w)
            try:
                #print(out)
                os.makedirs("out/"+out+"/z0/")
            except:
                pass
        if bounds_x != None and bounds_z != None:
            for x in range(bounds_x[0],bounds_x[1]+1):
                for y in range(bounds_z[0],bounds_z[1]+1):
                    if mode != "none":
                        numpy_render.make_tile(w,atlas,light_atlas,biome_atlas,"{},{}.zip".format(x,y),mode,out,config)
        if render_all:
            if mode != "none":
                for voxelfile in os.listdir(w):
                    if voxelfile.endswith('.zip'):
                        numpy_render.make_tile(w,atlas,light_atlas,biome_atlas,voxelfile,mode,out,config)
                #numpy_render.make_all_tiles(w,atlas,light_atlas,biome_atlas,mode,out)
    if len(world) > 1:
        # do merge code here
        merger.merge(world)
    if zoom > 0:
        stitch.zoom_stitch(zoom)
        pass
    if stitch_tiles:
        print("stitching")
        stitch.stitch(zoom)

    
    
    print("Done!")

if __name__ == "__main__":
    main(sys.argv[1:])
