from PIL import Image
import os
import json

import numpy as np

water_tint    = (63/255, 118/255, 228/255,1.0) #3F76E4
grass_tint    = (0.0, 0.0, 0.0,1.0) #91BD59
folliage_tint = (50/255, 171/255, 47/255,1.0) #77AB2F

def get_biome_atlas():
    image = Image.open("palettes/biome.png").convert('RGBA')
    biome_atlas = (np.asarray(image)/255)
    return biome_atlas


tints = get_biome_atlas()


def get_model_color(blockname,be = False,variation=""):
    pix = (0,0,0,0)

    filename = "assets/minecraft/models/{}.json".format(blockname)
    #print(blockname)
    f = open(filename)
    j = json.load(f)
    
    if "textures" in j:
        texture = j["textures"][next(iter( j["textures"]))]
        texture_to_open = ""
        if texture.startswith("minecraft:"):
            texture_to_open = "assets/minecraft/textures/{}.png".format(texture[10:])
        elif "top" in j["textures"]:
            texture_to_open = "assets/minecraft/textures/{}.png".format(j["textures"]["top"])
            #print("this has a top",texture_to_open)
        else:
            texture_to_open = "assets/minecraft/textures/{}.png".format(texture)

        if os.path.isfile(texture_to_open):
            
            img = Image.open(texture_to_open)
            img = img.convert("RGBA")
            img = img.resize((1,1))
            pix = img.getpixel((0,0))

    f.close()

    pixels = np.full((256,4),pix)

    if blockname[6:] in ["grass_block","grass","tall_grass","sugarcane","fern","large_fern","tall_grass_top","tall_grass_bottom","large_fern_top","large_fern_bottom"]:
        pixels = (pixels * tints[0]).astype(np.uint8)
    if blockname[6:]  in ["oak_leaves","acacia_leaves","dark_oak_leaves","vines","jungle_leaves"]:
        pixels = (pixels * tints[1]).astype(np.uint8)
    if blockname[6:]  == "water":
        if be:
            pixels = (pixels * tints[3]).astype(np.uint8)
        else:
            pixels = (pixels * tints[2]).astype(np.uint8)
        #print(blockname,pixels)
    if blockname[6:] == "spruce_leaves":
        pixels = (pixels * (97/255, 153/255, 97/255,1.0)).astype(np.uint8)
    if blockname[6:] == "birch_leaves":
        pixels = (pixels * (128/255, 167/255, 85/255,1.0)).astype(np.uint8)
    if blockname[6:] == "lily_pad":
        pixels = (pixels * (32/255, 128/255, 48/255,1.0)).astype(np.uint8)
    
    return pixels

def get_atlas(be = False):
    atlas = {"minecraft:air": np.zeros((256,4))}
    #print(atlas["minecraft:air"].shape)

    directory = "assets/minecraft/blockstates/"

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            blockname = "minecraft:{}".format(filename.split(".")[0])
            #print(filename)
            f = open(directory+filename)
            j = json.load(f)
            f.close()
            first=True
            if "variants" in j:
                #print(j["variants"])
                for item in j["variants"].items():
                    modelname = ""
                    variation = ""
                    if type(item[1]) is list:
                        modelname = item[1][0]["model"]
                    else:
                        modelname = item[1]["model"]
                        variation = item[0]
                    if (modelname.startswith("minecraft:")):
                        pix = get_model_color(modelname[10:],be)

                        #rint("printed",modelname,pix[0])
                        if variation != "":
                            s = blockname+"["+variation+"]"
                            atlas[s] = pix
                            
                        if variation == "" or first == True:
                            atlas[blockname] = pix
                            first = False
                        #break
                    else:
                        print(modelname)
            elif "multipart" in j:
                modelname = ""
                #print("{} is a multipart".format(blockname))
                if type(j["multipart"][0]["apply"]) is list:
                    modelname = j["multipart"][0]["apply"][0]["model"]
                else:
                    modelname = j["multipart"][0]["apply"]["model"]

                if (modelname.startswith("minecraft:")):
                    pix = get_model_color(modelname[10:],be)
                        
                    atlas[blockname] = pix             
                else:
                    print(modelname)
            else:
                print("Nothing found for {} ???".format(blockname))
            
    print("Generated pixel atlas with {} blocks".format(len(atlas)))
    #print(atlas.keys())
    return atlas

def get_light_atlas(light):
    image = Image.open("palettes/{}.png".format(light)).convert('RGBA')
    #light_atlas = np.ones((16,16,4))

    light_atlas = np.asarray(image)/255
    #print(light_atlas)
    return light_atlas

