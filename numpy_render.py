from PIL import Image
import numpy as np
from zipfile import ZipFile
import os

from numpy.core.arrayprint import array_str

#import atlas_gen

#import atlas_gen_2
import read_key

#atlas = atlas_gen_2.get_atlas()

# ------------------------
# Cache parsing routines
# ------------------------

def cache_height(lay):
    return np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*0 + lay * 256*256*4).reshape(256,256) - 1 # -1 to fix y=256 terrain

def cache_blockid(lay):
    data_ih = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*1 + lay * 256*256*4).reshape(256,256)
    data_il = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*2 + lay * 256*256*4).reshape(256,256)
    return 256*data_ih + data_il

def cache_light(lay):
    data_l = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*3 + lay * 256*256*4).reshape(256,256)
    return data_l,(data_l & 240) >> 4,(data_l & 15)

def cache_biome():
    return np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*17).reshape(256,256)

# ----------------------
# Tile Rendering Routines
# ----------------------

def render_land():
    land_color  = [184, 184, 184,255]
    water_color = [126, 150, 223,255]

    water = read_key.keys_to_water_id()
    layers = []

    darkness = 0
    
    lay = 0
    data_h = cache_height(0)
    data_i = cache_blockid(0)

    data_sealevel = np.zeros((256,256))
    data_sealevel[:,:] = np.where(data_h[:,:] == 64,1,0)
    data_water     = np.where(data_i == water, 0,1)
    data_void     = np.where(data_i == 0, 0,1)
    
    land_map = np.zeros([256,256,4],dtype=np.uint8)

    zero_channel = np.zeros_like(data_h)
    land_map  = (np.stack([data_water, data_water, data_water,data_void*data_water], axis=2) * land_color).astype(np.uint8)
    water_map = (np.stack([data_water==0, data_water==0, data_water==0,data_void*(data_water==0)], axis=2) * water_color).astype(np.uint8)

    return Image.fromarray(land_map+water_map,"RGBA")

def render_biome(biome_atlas):
    data_b = cache_biome()
    img_b = (biome_atlas[4][data_b] * 255 ).astype(np.uint8)
    return Image.fromarray(img_b)

def render_height(config):
    cut=0
    if 'cut' in config:
        cut = config['cut']
    render_layer=None
    if 'render_layer' in config:
        render_layer = config['render_layer']

    water = read_key.keys_to_water_id()

    data_h = cache_height(0)
    data_h_w = cache_height(1)

    data_h -= data_h % cut
    data_h_w -= data_h_w % cut

    data_i = cache_blockid(0)    
    data_void = np.where(data_i == 0, 0,1)

    data_water = np.where(data_i == water, 0, 1).astype(np.uint8)

    zero_channel = np.zeros_like(data_h)
    height_map = np.stack([data_h*data_water, data_h*data_water, data_h*data_water,((data_void*255) * data_water).astype(np.uint8)], axis=2)
    height_map_w = np.stack([data_h_w*(data_water==0), data_h_w*(data_water==0), data_h_w*(data_water==0),((data_void*255) * (data_water==0)).astype(np.uint8)], axis=2)

    if render_layer == 0:
        return Image.fromarray(height_map)
    elif render_layer == 1:
        return Image.fromarray(height_map_w)
    else:
        return Image.fromarray(height_map_w+height_map)

def render_light():
    data_l,data_ls,data_lb = cache_light(0)    
    return Image.fromarray(data_lb*16)

def render_terrain(atlas,light_atlas,biome_atlas,config):
    render_layer=None
    if 'render_layer' in config:
        render_layer = config['render_layer']


    color_map,water = read_key.keys_to_atlas_color(atlas)
    layers = []

    darkness = 0
    data_b = cache_biome()

    for lay in range(4):
        data_h = cache_height(lay)
        data_i = cache_blockid(lay)
        data_l,data_ls,data_lb = cache_light(lay)

        s_tint = np.ones((256,256))

        if lay == 0 or lay == 1:
            s_tint[1:,:] = np.where(data_h[1:,:] > data_h[:-1,:],1.1,s_tint[1:,:]) # Check UP
            s_tint[:,:-1] = np.where(data_h[:,:-1] > data_h[:,1:], 1.1, s_tint[:,:-1])# Check Right
            s_tint[:-1,:] = np.where(data_h[:-1,:] > data_h[1:,:],0.85,s_tint[:-1,:]) # Check Down
            s_tint[:,1:] = np.where(data_h[:,1:] > data_h[:,:-1], 0.85, s_tint[:,1:]) # Check Left       
        
        im = color_map[data_i,data_b]
        
        h_tint = 1
        if config['y_shading'] == True:
            h_tint = 0.9 + ((data_h)/255)*0.45

        l_tint = light_atlas[data_ls,data_lb]
        
        im = im.astype(float)

        im[:,:,0] = ((im[:,:,0] * h_tint * s_tint))
        im[:,:,1] = ((im[:,:,1] * h_tint * s_tint))
        im[:,:,2] = ((im[:,:,2] * h_tint * s_tint))

        im = im*l_tint

        im = im.clip(0,255).astype(np.uint8)

        img = im
        layers.append(img)

    layers[1][:,:,3] = np.where(layers[0][:,:,3] > 0, 255, layers[1][:,:,3])
    
    out_render = Image.new("RGBA",(256,256))
    
    if render_layer == 1 or render_layer == None:
        out_render = Image.fromarray(layers[1])
    if render_layer == 0 or render_layer == None:
        out_render = Image.alpha_composite(out_render,Image.fromarray(layers[0]))
    if render_layer == 2 or render_layer == None:
        out_render = Image.alpha_composite(out_render,Image.fromarray(layers[2]))
    if render_layer == 3 or render_layer == None:
        out_render = Image.alpha_composite(out_render,Image.fromarray(layers[3]))
    
    return out_render

# ---------------
#   Find and uncompress tiles
# ---------------

def render_tile(atlas,light_atlas,biome_atlas,mode,config={}):

    if mode == "biome":
        return render_biome(biome_atlas)
    if mode == "height":
        return render_height(config)
    if mode == "light":
        return render_light()
    if mode == "land":
        return render_land()
    else:
        return render_terrain(atlas,light_atlas,biome_atlas,config)

def make_tile(world,atlas,light_atlas,biome_atlas,voxelfile,mode,out,config={}):
    print(voxelfile)
    voxeldirectory = "{}".format(world)
    try:
        with ZipFile("{}/{}".format(voxeldirectory,voxelfile),'r') as zip:
            zip.extractall("temp/")
        render_tile(atlas,light_atlas,biome_atlas,mode,config).save("out/{}z0/{}.png".format(out,voxelfile[:-4]))
    except Exception as e:
        print(e)
    return