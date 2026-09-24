from PIL import Image, ImageDraw, ImageFilter
import math, os, random

ROOT=os.path.dirname(__file__)
TEMPLATE=os.path.join(ROOT,"..","template.png")
OUT=ROOT
W=H=1024

tpl=Image.open(TEMPLATE).convert("RGB").resize((W,H))
p=tpl.load()
mask=Image.new("L",(W,H),0); mp=mask.load()
for y in range(H):
    for x in range(W):
        r,g,b=p[x,y]
        mp[x,y]=255 if (r>220 and g>220 and b>220) else 0
mask=mask.filter(ImageFilter.GaussianBlur(0.35))

def lerp(a,b,t): return int(a+(b-a)*t)

def gradient(c1,c2):
    im=Image.new("RGB",(W,H)); px=im.load()
    for y in range(H):
        for x in range(W):
            t=(0.62*y/H+0.38*abs(x-W/2)/(W/2))
            px[x,y]=tuple(lerp(c1[i],c2[i],min(1,t)) for i in range(3))
    return im

def reactor(draw,cx,cy,r,cyan):
    for rr,w in [(r,3),(int(r*.72),2),(int(r*.42),2)]:
        draw.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline=cyan,width=w)
    for a in range(0,360,30):
        a=math.radians(a)
        x1=cx+math.cos(a)*r*.48; y1=cy+math.sin(a)*r*.48
        x2=cx+math.cos(a)*r*.88; y2=cy+math.sin(a)*r*.88
        draw.line((x1,y1,x2,y2),fill=cyan,width=2)
    draw.ellipse((cx-r*.18,cy-r*.18,cx+r*.18,cy+r*.18),fill=(220,250,255))

def circuits(draw, cyan, seed):
    random.seed(seed)
    for side in [0,1]:
        xs=range(90,430,55) if side==0 else range(594,934,55)
        for x in xs:
            y=random.randint(120,260)
            pts=[(x,y)]
            for _ in range(4):
                y+=random.randint(55,110)
                x2=x+random.choice([-35,0,35])
                pts.extend([(x,y-18),(x2,y+18)])
                x=x2
            draw.line(pts,fill=cyan,width=2)
            for qx,qy in pts[::3]:
                draw.ellipse((qx-3,qy-3,qx+3,qy+3),fill=cyan)

def make(name, base1,base2,metal,accent,cyan, mode="classic"):
    tex=gradient(base1,base2)
    d=ImageDraw.Draw(tex,"RGB")
    # metallic center accents
    d.polygon([(430,100),(512,72),(594,100),(566,340),(512,305),(458,340)],fill=metal)
    d.polygon([(405,865),(512,835),(619,865),(600,950),(424,950)],fill=metal)
    # armor diagonals
    for off in [0,512]:
        for y in [185,350,520,690]:
            d.polygon([(70+off,y),(165+off,y-35),(205+off,y-5),(115+off,y+40)],fill=accent)
    # luminous rails
    for x in [220,512,804]:
        d.line((x,70,x,950),fill=cyan,width=4)
        d.line((x+7,70,x+7,950),fill=(20,45,60),width=2)
    circuits(d,cyan,42 if "Arc" in name else 84)
    reactor(d,512,690,58,cyan)
    reactor(d,150,505,32,cyan); reactor(d,874,505,32,cyan)
    # subtle panel scratches / tech seams
    for y in range(120,930,80):
        d.line((80,y,330,y-20),fill=(80,80,85),width=1)
        d.line((694,y-20,944,y),fill=(80,80,85),width=1)
    # masked result on black background
    out=Image.new("RGB",(W,H),(0,0,0))
    out.paste(tex,(0,0),mask)
    # crisp mask edge retained by template silhouette
    out.save(os.path.join(OUT,name),optimize=True,compress_level=9)

make("JarvisMobil_Mark85_v1.png",
     (74,5,8),(18,8,10),(185,130,48),(105,18,18),(92,220,255))
make("JarvisMobil_ArcBlue_v1.png",
     (3,34,62),(3,9,18),(170,185,195),(4,78,132),(80,225,255))
print("generated")

make("JarvisMobil_ArcBlue_v2.png",
     (2,28,52),(2,7,15),(105,125,140),(3,62,110),(76,232,255),"energy")
make("JarvisMobil_ArcCore_v3.png",
     (1,18,34),(1,4,10),(55,72,86),(5,40,78),(115,245,255),"energy")
make("JarvisMobil_Experimental_v4.png",
     (8,8,12),(2,2,5),(112,125,135),(20,36,52),(0,245,255),"hud")
make("JarvisMobil_TP1_v5.png",
     (9,17,24),(2,5,8),(180,185,188),(34,48,58),(90,220,235),"tp1")

def make_jarvis_arc_v2():
    tex=gradient((1,12,24),(0,2,7))
    d=ImageDraw.Draw(tex,"RGB")
    cyan=(80,238,255); ice=(205,248,255); gun=(28,48,62)
    for i in range(7):
        y=150+i*105
        d.arc((35,y-90,475,y+115),205,345,fill=cyan,width=3+(i%2))
        d.arc((549,y-115,989,y+90),15,155,fill=cyan,width=3+(i%2))
    d.polygon([(492,70),(512,48),(532,70),(526,360),(512,395),(498,360)],fill=gun)
    d.line((512,58,512,402),fill=ice,width=5)
    for pts in [[(78,180),(270,105),(360,150),(205,245)],[(946,180),(754,105),(664,150),(819,245)],[(65,470),(245,405),(335,470),(190,555)],[(959,470),(779,405),(689,470),(834,555)],[(90,760),(255,680),(340,735),(205,825)],[(934,760),(769,680),(684,735),(819,825)]]:
        d.polygon(pts,fill=gun)
    reactor(d,512,690,36,cyan)
    reactor(d,164,510,19,cyan); reactor(d,860,510,19,cyan)
    for x in (115,205,819,909):
        for y in range(220,820,150):
            d.line((x-16,y,x+16,y),fill=ice,width=2)
            d.ellipse((x-3,y-3,x+3,y+3),fill=ice)
    d.line((230,120,330,880),fill=(24,105,135),width=2)
    d.line((794,120,694,880),fill=(24,105,135),width=2)
    out=Image.new("RGB",(W,H),(0,0,0))
    out.paste(tex,(0,0),mask)
    out.save(os.path.join(OUT,"JarvisMobil_JARVIS_ARC_v2.png"),optimize=True,compress_level=9)
make_jarvis_arc_v2()
