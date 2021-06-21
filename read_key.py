import numpy as np
def keys_to_atlas_color(atlas):
    file = open("temp/key",'r')
    keys = file.readlines()
    file.close

    color_map = np.zeros( (len(keys)+1,256,4))
    #color_map = np.zeros((len(keys)+1,4))
    #print(color_map.shape)
    water = -1

    for i in range(len(keys)):
        wah = keys[i].split('}')[1].split(']')[0]
        weh = keys[i].split('{', 1)[1].split('}')[0]
        wuh = ""
        if "[" in keys[i]:
            wuh = keys[i].split('[',1)[1].split(']')[0]
        if weh+"["+wuh+"]" in atlas:
            key_color = atlas[weh+"["+wuh+"]"]
        else:
            key_color = atlas[weh]

        '''
        if 'waterlogged=true' in wuh or weh in ['minecraft:seagrass','minecraft:kelp']:
            color_map[i+1] = key_color[:256]
        else:
            #color_map[i+1] = atlas['minecraft:water'][256:]
            color_map[i+1] = key_color[:256]
        '''
        color_map[i+1] = key_color
       #print(weh,atlas[weh][0])
        if weh == "minecraft:water" and wah == "[level=0":
            water = i + 1
    
    return color_map,water

def keys_to_water_id():
    file = open("temp/key",'r')
    keys = file.readlines()
    file.close
    water = -1

    for i in range(len(keys)):
        wah = keys[i].split('}')[1].split(']')[0]
        weh = keys[i].split('{', 1)[1].split('}')[0]
        if weh == "minecraft:water" and wah == "[level=0":
            water = i + 1
            break
    return water
