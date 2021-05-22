import math
from PIL import Image
import os.path

def stitch(zoom):
    sx=0
    sy=0
    ex=0
    ey=0

    ts = 256 # tile size
    dir = "out/z{}".format(zoom)
    first = True
    for t in os.listdir(dir):
        print(t)
        tx = int(t.split(".")[0].split(",")[0])
        tz = int(t.split(".")[0].split(",")[1])
        if first:
            sx = tx
            sy = tz
            ex = tx
            ey = tz
            first = False
        else:
            if tx < sx:
                sx = tx
            if tz < sy:
                sy = tz
            if tx > ex:
                ex = tx
            if tz > ey:
                ey = tz

    
    s_x = (ex-sx + 1) * ts
    s_z = (ey-sy + 1) * ts
    print(sx,sy,ex,ey,s_x,s_z)

    print(s_x,s_z)

    map_img = Image.new(mode="RGBA", size = (s_x,s_z), color = (0,0,0,0))

    print("Stitching Together a {}x{} Image".format(s_x,s_z))

    for x_t in range(sx,ex+1):
        for y_t in range(sy,ey+1):
            filename = "{}/{},{}.png".format(dir,x_t,y_t)
            print(filename)
            if os.path.isfile(filename):
                paste_img = Image.open(filename)
                Image.Image.paste(map_img,paste_img,((x_t - sx)*ts, (y_t - sy)*ts))

    #map_img.show()
    
    map_img.save("out/out.png")

def zoom_stitch(zoom):
    for i in range(zoom):
        try:
            os.makedirs('out/z{}'.format(i+1))
        except:
            pass
        dir = "out/z{}".format(i)
        print("making zoom {}".format(i+1))
        zTiles = {}
        for tile in os.listdir(dir):
            if (",") in tile:
                x = int(tile.split(".")[0].split(",")[0])
                z = int(tile.split(".")[0].split(",")[1])
                tn = "{},{}.png".format(str(math.floor(x/2)),str(math.floor(z/2)))
                if tn in zTiles:
                    zTiles[tn].append(tile)
                else:
                    zTiles[tn] = [tile]
        
        for t in zTiles:
            tx = int(t.split(".")[0].split(",")[0])
            tz = int(t.split(".")[0].split(",")[1])
            im = Image.new("RGBA",(512,512),(0,0,0,0))
            for st in zTiles[t]:
                stx = int(st.split(".")[0].split(",")[0])
                stz = int(st.split(".")[0].split(",")[1])
                #print(tx*2,tz*2,stx,stz)
                imp = Image.open("{}/{}".format(dir,st))
                
                im.paste(imp,((stx-tx*2)*256,(stz-tz*2)*256))
            im = im.resize((256,256))
            im.save("out/z{}/{}".format(i+1,t))
