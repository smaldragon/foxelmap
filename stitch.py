from PIL import Image
import os.path

def stitch(sx,ex,sy,ey):
    ts = 256 # tile size

    s_x = (ex-sx + 1) * ts
    s_z = (ey-sy + 1) * ts

    print(s_x,s_z)

    map_img = Image.new(mode="RGB", size = (s_x,s_z), color = (0,0,0))

    print("Stitching Together a {}x{} Image".format(s_x,s_z))

    for x_t in range(sx,ex+1):
        for y_t in range(sy,ey+1):
            filename = "out/{},{}.png".format(x_t,y_t)
            #print(filename)
            if os.path.isfile(filename):
                paste_img = Image.open(filename)
                Image.Image.paste(map_img,paste_img,((x_t - sx)*ts, (y_t - sy)*ts))

    #map_img.show()
    
    map_img.save("out/out.png")
