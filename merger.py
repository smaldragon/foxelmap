import os
import shutil
from PIL import Image

def merge(world):
    print("merging")
    merge_atlas = {}

    for w in world:
        for t in os.listdir(w):
            path = w+"/"+t
            mtime = os.path.getmtime(path)
            f = t[:-4]
            if f in merge_atlas:
                merge_atlas[f].append((w,mtime))
            else:
                merge_atlas[f] = [(w,mtime)]
    merge_keys = merge_atlas.keys()
    for key in merge_keys:
        count = len(merge_atlas[key])
        if count == 1:
            d = "out/"+merge_atlas[key][0][0]+"/z0/"+key+".png"
            if os.path.isfile(d):
                shutil.copy(d,'out/z0/'+key+".png")
        else:
            img = Image.new("RGBA",(256,256),(0,0,0,0))
            ksort = merge_atlas[key].copy()
            save = False
            while len(ksort) > 0:
                recentI = 0
                recentT = 0
                for i in range(len(ksort)):
                    if ksort[i][1] > recentT:
                        recentI = i
                        recentT = ksort[i][1]
                d = "out/"+ksort[recentI][0]+"/z0/"+key+".png"
                if os.path.isfile(d):
                    img = Image.alpha_composite(img,Image.open(d))
                    save = True
                ksort.pop(recentI)

            if save:
                img.save('out/z0/'+key+".png")

    '''
    merge_dir = "caches"
    for dirName, subdirList, fileList in os.walk(merge_dir):
        if dirName.endswith("\overworld"):
            print(dirName)
            for file in fileList:
                mtime = os.path.getmtime(dirName+"/"+file)
                #print(file,time)
                if file in merge_atlas:
                    merge_atlas[file].append((dirName,mtime))
                else:
                    merge_atlas[file] = [(dirName,mtime)]
    '''