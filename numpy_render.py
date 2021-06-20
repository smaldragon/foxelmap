from PIL import Image
import numpy as np
from zipfile import ZipFile
import os

from numpy.core.arrayprint import array_str

#import atlas_gen

#import atlas_gen_2
import read_key

#atlas = atlas_gen_2.get_atlas()

def render_land():
    land_color = [184, 184, 184,255]
    water_color = [254, 254, 254,255]

    water = read_key.keys_to_water_id()
    layers = []

    darkness = 0
    
    lay = 0
    data_h = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*0 + lay * 256*256*4).reshape(256,256)
    data_ih = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*1 + lay * 256*256*4).reshape(256,256)
    data_il = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*2 + lay * 256*256*4).reshape(256,256)
    data_i = 256*data_ih + data_il

    data_sealevel = np.zeros((256,256))
    data_sealevel[:,:] = np.where(data_h[:,:] == 64,1,0)
    data_water     = np.where(data_i == water, 1,0)
    data_seawater = ((data_sealevel * data_water) - 1 ) * -1
    data_void     = np.where(data_i == 0, 1,0)
    land_map = np.zeros([256,256,4],dtype=np.uint8)
    
    for x in range(256):
        for z in range(256):
            if data_void[x,z] == 0:
                if data_seawater[x,z] == 0:
                    land_map[x,z] = land_color
                else:
                    land_map[x,z] = water_color

    return Image.fromarray(land_map,"RGBA")

def render_biome(biome_atlas):
    data_b = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*17).reshape(256,256)
    #img_b = np.zeros((256,256,4),np.uint8)
    img_b = (biome_atlas[4][data_b] * 255 ).astype(np.uint8)
    return Image.fromarray(img_b)

def render_height():
    water = read_key.keys_to_water_id()

    data_h =   np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*0).reshape(256,256)
    data_h_w = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*0 + 256*256*4).reshape(256,256)

    data_ih = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*1).reshape(256,256)
    data_il = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*2).reshape(256,256)
    data_i = 256*data_ih + data_il

    
    data_void = np.where(data_i == 0, 0,1)
    data_water = np.where(data_i == water, 0, 1).astype(np.uint8)

    zero_channel = np.zeros_like(data_h)
    height_map = np.stack([data_h*data_water, data_h*data_water, data_h*data_water,((data_void*255) * data_water).astype(np.uint8)], axis=2)
    height_map_w = np.stack([data_h_w*(data_water==0), data_h_w*(data_water==0), data_h_w*(data_water==0),((data_void*255) * (data_water==0)).astype(np.uint8)], axis=2)

    
    return Image.fromarray(height_map_w+height_map)

def render_light():
    data_l = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*3).reshape(256,256)
    data_l = (data_l & 15) << 4
    return Image.fromarray(data_l)

def render_terrain(atlas,light_atlas,biome_atlas,render_layer=None):
    #light_atlas = atlas_gen_3.get_light_atlas() # this shouldnt be called in this script ?

    color_map,water = read_key.keys_to_atlas_color(atlas)
    layers = []

    darkness = 0

    data_b = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*17).reshape(256,256)
    #Image.fromarray(data_b*100).save("wow.png")
    
    for lay in range(4):
        data_h = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*0 + lay * 256*256*4).reshape(256,256)
        #data_h = np.where(data_h == 0, 255, data_h)
        data_ih = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*1 + lay * 256*256*4).reshape(256,256)
        data_il = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*2 + lay * 256*256*4).reshape(256,256)
        data_i = 256*data_ih + data_il
        data_l = np.fromfile("temp/data",dtype='uint8',count=256*256,offset=256*256*3 + lay * 256*256*4).reshape(256,256)
        data_ls = (data_l & 240) >> 4
        data_lb = (data_l & 15)


        #imh = Image.fromarray(data_h)
        #imh.save("terrain_{}.png".format(lay))
        
        s_tint = np.ones((256,256))

        if lay == 0 or lay == 1:
            s_tint[1:,:] = np.where(data_h[1:,:] > data_h[:-1,:],1.1,s_tint[1:,:]) # Check UP
            s_tint[:,:-1] = np.where(data_h[:,:-1] > data_h[:,1:], 1.1, s_tint[:,:-1])# Check Right
            s_tint[:-1,:] = np.where(data_h[:-1,:] > data_h[1:,:],0.85,s_tint[:-1,:]) # Check Down
            s_tint[:,1:] = np.where(data_h[:,1:] > data_h[:,:-1], 0.85, s_tint[:,1:]) # Check Left       
        
        im = np.zeros( (256,256,4), dtype=float)

        im = color_map[data_i,data_b]
        #if lay == 0:
        #    im[:,:,3] = np.where(data_i[:,:] == water, im[:,:,3], 255)
        #    im[:,:,3] = np.where(data_i[:,:] != 0, im[:,:,3], 0)
        '''for i in np.ndindex(data_i.shape):
            c_d = color_map[data_i[i]]
            if lay == 0 and data_i[i] != water and data_i[i] != 0:
                c_d = (c_d[0],c_d[1],c_d[2],255)
            im[i]=c_d
        '''

        h_tint = 1.0
        
        l_tint = 1.0
        h_tint = 0.9 + ((data_h)/255)*0.45
        #h_tint = 0.9 + (([data_h,data_h,data_h,255])/255)*0.45
        #l_tint = np.maximum((data_ls+darkness*16)*1.0,data_lb*1.0)/255
        l_tint = light_atlas[data_ls,data_lb]
        
        im = im.astype(float)

        im[:,:,0] = ((im[:,:,0] * h_tint * s_tint))
        im[:,:,1] = ((im[:,:,1] * h_tint * s_tint))
        im[:,:,2] = ((im[:,:,2] * h_tint * s_tint))

        im = im*l_tint

        im = im.clip(0,255).astype(np.uint8)

        #img = Image.fromarray(im)
        img = im
        #img.save('blocks_{}.png'.format(lay))
        layers.append(img)

    layers[1][:,:,3] = np.where(layers[0][:,:,3] > 0, 255, layers[1][:,:,3])
    
    out_render = Image.new("RGBA",(256,256))
    #render_layer = 1
    if render_layer == 1 or render_layer == None:
        out_render = Image.fromarray(layers[1])
    if render_layer == 0 or render_layer == None:
        out_render = Image.alpha_composite(out_render,Image.fromarray(layers[0]))
    if render_layer == 2 or render_layer == None:
        out_render = Image.alpha_composite(out_render,Image.fromarray(layers[2]))
    if render_layer == 3 or render_layer == None:
        out_render = Image.alpha_composite(out_render,Image.fromarray(layers[3]))
    return out_render

def render_tile(atlas,light_atlas,biome_atlas,mode):

    if mode == "biome":
        return render_biome(biome_atlas)
    if mode == "height":
        return render_height()
    if mode == "light":
        return render_light()
    if mode == "land":
        return render_land()
    else:
        return render_terrain(atlas,light_atlas,biome_atlas)

'''
voxeldirectory = "NoteBlcoks/overworld/"
with ZipFile(voxeldirectory+"-25,13.zip",'r') as zip:
    zip.extractall()
    #render_tile().show()
    render_tile().save("debug_render_tile.png")
'''


def make_tile(world,atlas,light_atlas,biome_atlas,x,y,mode,out):
    voxeldirectory = "{}".format(world)    
    try:
        with ZipFile("{}/{},{}.zip".format(voxeldirectory,x,y),'r') as zip:
            zip.extractall("temp/")
        
        render_tile(atlas,light_atlas,biome_atlas,mode).save("out/{}z0/{},{}.png".format(out,x,y))
        print("out/z0/{},{}.png".format(x,y))
    except Exception as e:
        print(e)
        #Image.new(mode ="RGBA",size =(256,256),color=(0,0,0,0)).save("out/z0/{},{}.png".format(x,y))
    return
    '''
    with ZipFile("{}/{},{}.zip".format(voxeldirectory,x,y),'r') as zip:
        zip.extractall()
    print("{},{}.zip".format(x,y))
    render_tile(atlas).save("out/z0/{},{}.png".format(x,y))
    print("out/z0/{},{}.png".format(x,y))
    return
    '''
    
def make_all_tiles(world,atlas,light_atlas,biome_atlas,mode,out):
    
    voxeldirectory = "{}".format(world)
    with ZipFile("{}/-18,13.zip".format(voxeldirectory),'r') as zip:
        zip.extractall("temp/")

    for voxelfile in os.listdir(voxeldirectory):
        print(voxeldirectory)
        if voxelfile.endswith(".zip"):
            with ZipFile("{}/{}".format(voxeldirectory,voxelfile),'r') as zip:
                zip.extractall("temp/")

        render_tile(atlas,light_atlas,biome_atlas,mode).save("out/{}z0/{}.png".format(out,voxelfile[:-4]))
'''
    for voxelfile in os.listdir(voxeldirectory):
        print(voxelfile)
        if voxelfile.endswith(".zip"):
            with ZipFile(voxeldirectory+voxelfile,'r') as zip:
                zip.extractall()

        render_tile().save("z1-numpy/{}.png".format(voxelfile))
'''
