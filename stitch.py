import math
from PIL import Image
import os.path

## Joins and shrinks out tiles to make different zoom levels
def zoom_stitch(zoom,render_all,bounds_x,bounds_z):
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
                if render_all or (
                    x >= math.floor(bounds_x[0]/(i+1)) and
                    z >= math.floor(bounds_z[0]/(i+1)) and
                    x <= math.floor(bounds_x[1]/(i+1)) and
                    z <= math.floor(bounds_z[1]/(i+1))
                ):
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

## Joins the highest zoom level tiles into a single image
def stitch(zoom,render_all,bounds_x,bounds_z):
    ts = 256 # tile size
    dir = "out/z{}".format(zoom)
    if not render_all:
        sx=math.floor(bounds_x[0]/(2**zoom))
        sz=math.floor(bounds_z[0]/(2**zoom))
        ex=math.floor(bounds_x[1]/(2**zoom))
        ez=math.floor(bounds_z[1]/(2**zoom))
    else:
        first = True
        for t in os.listdir(dir):
            print(t)
            tx = int(t.split(".")[0].split(",")[0])
            tz = int(t.split(".")[0].split(",")[1])
            if first:
                sx = tx
                sz = tz
                ex = tx
                ez = tz
                first = False
            else:
                if tx < sx:
                    sx = tx
                if tz < sz:
                    sz = tz
                if tx > ex:
                    ex = tx
                if tz > ez:
                    ez = tz

    
    s_x = (ex-sx + 1) * ts
    s_z = (ez-sz + 1) * ts
    print(sx,sz,ex,ez,s_x,s_z)

    print(s_x,s_z)

    map_img = Image.new(mode="RGBA", size = (s_x,s_z), color = (0,0,0,0))

    print("Stitching Together a {}x{} Image".format(s_x,s_z))

    for x_t in range(sx,ex+1):
        for y_t in range(sz,ez+1):
            filename = "{}/{},{}.png".format(dir,x_t,y_t)
            print(filename)
            if os.path.isfile(filename):
                paste_img = Image.open(filename)
                Image.Image.paste(map_img,paste_img,((x_t - sx)*ts, (y_t - sz)*ts))

    #map_img.show()
    
    map_img.save("out/out.png")