import numpy as np
# === Water Tint =======
def get_water_tint_je():
    # default #3F76E4
    tint = np.full((256,4),(63, 118, 228,255))
    #tint[0] = (255,0,0,255)
    #tint[0] = (23, 135, 212,255)
    # cold ocean/ deep cold ocean #3D57D6
    tint[46] = (61, 87, 214, 255)
    tint[49] = (61, 87, 214, 255)
    # frozen ocean/deep fr ocean/frozen river #3938C9
    tint[10] = (57, 56, 201, 255)
    tint[11] = (57, 56, 201, 255)
    tint[50] = (57, 56, 201, 255)
    # lukewarm oceans #45ADF2
    tint[45] =(69, 173, 242, 255)
    tint[48] =(69, 173, 242, 255)
    # swamp #617B64
    tint[6]    = (97, 123, 100, 255)
    tint[134]  = (97, 123, 100, 255)
    # warm oceans #43D5EE
    tint[44] = (67, 213, 238, 255)
    tint[47] = (67, 213, 238, 255)

    return tint

def get_folliage_tint():
    #default (inventory) #77AB2F
    tint = np.full((256,4),(119, 171, 47,255)) 
    return tint

def get_grass_tint():
    #default (inventory) #7CBD6B
    tint = np.full((256,4),(124, 189, 107,255))
    tint[1] = (145, 189, 89,255)
    # badlands #90814D (144, 129, 77)
    tint[37] = (144, 129, 77,255)
    tint[38] = (144, 129, 77,255)
    tint[39] = (144, 129, 77,255)
    tint[165] = (144, 129, 77,255)
    tint[166] = (144, 129, 77,255)
    tint[167] = (144, 129, 77,255)
    # deserts and savannas and nether #BFB755 (191, 183, 85)
    # jungle #59C93C (89, 201, 60)
    # jungle edge #64C73F (100, 199, 63)
    # forest, flower forest, wooded hills (121, 192, 90) #79C05A
    # birch forest(s) #88BB67 (136, 187, 103)
    # dark forest 507A32 (80, 122, 50)
    # swamps(s) #4C763C (76, 118, 60)
    # plains/sunflower plains / beach 91BD59 (145, 189, 89)
    # oceans end and void (142, 185, 113) #8EB971 
    # mushroom islands #55C93F (85, 201, 63)
    # mountains (138, 182, 137)
    
    return tint
def get_admist_tint():
    tint = np.full((256,4),(0, 0, 0,255))
    tint[0] = (0,0,112, 255) #000070
    tint[1] = (141, 179, 96, 255) #8db360
    tint[2] = (250, 148, 24, 255) #fa9418
    return tint

def get_tints():
    tints = np.concatenate([[get_grass_tint()],[get_folliage_tint()],[get_water_tint_je()],[get_admist_tint()]]) / 255
    return tints
