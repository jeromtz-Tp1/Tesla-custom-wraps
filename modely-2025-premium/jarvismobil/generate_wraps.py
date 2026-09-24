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

# V3 ARMOR — rebuilt from scratch after in-car V2 review.
def make_armor_v3():
    tex=gradient((4,22,34),(1,4,8))
    d=ImageDraw.Draw(tex,"RGB")
    cyan=(75,235,255); glow=(205,252,255); titanium=(42,58,68); blue=(7,62,91)
    # Large interlocking armor plates; broad shapes survive Tesla 3D rendering.
    plates=[
      [(55,120),(245,65),(410,135),(325,300),(105,285)],
      [(969,120),(779,65),(614,135),(699,300),(919,285)],
      [(70,335),(275,305),(405,430),(300,590),(85,555)],
      [(954,335),(749,305),(619,430),(724,590),(939,555)],
      [(85,610),(300,600),(405,730),(290,900),(100,845)],
      [(939,610),(724,600),(619,730),(734,900),(924,845)]
    ]
    for i,p in enumerate(plates):
        d.polygon(p,fill=titanium if i%2==0 else blue)
        # cyan seam only on one edge, not random cracks
        d.line(p[:3],fill=cyan,width=5)
    # central dark armored spine, no silver racing stripe
    d.polygon([(450,55),(512,30),(574,55),(552,390),(512,430),(472,390)],fill=(10,17,22))
    d.line((512,42,512,420),fill=cyan,width=3)
    # angular energy vents
    for cx,sgn in [(205,1),(819,-1)]:
        for yy in (245,500,755):
            pts=[(cx,yy),(cx+sgn*72,yy+26),(cx+sgn*35,yy+55)]
            d.line(pts,fill=glow,width=4)
    # compact triangular AI cores integrated into armor
    for cx,cy,s in [(512,700,44),(170,505,25),(854,505,25)]:
        pts=[(cx,cy-s),(cx-s,cy+s),(cx+s,cy+s),(cx,cy-s)]
        d.line(pts,fill=cyan,width=5)
        d.polygon([(cx,cy-int(s*.45)),(cx-int(s*.42),cy+int(s*.42)),(cx+int(s*.42),cy+int(s*.42))],fill=(18,90,110))
        d.ellipse((cx-5,cy-5,cx+5,cy+5),fill=glow)
    # restrained HUD glyph bars
    for x in (125,899):
        for y in (180,390,600,810):
            d.line((x-24,y,x+24,y),fill=(100,210,225),width=2)
    out=Image.new("RGB",(W,H),(0,0,0))
    out.paste(tex,(0,0),mask)
    out.save(os.path.join(OUT,"JarvisMobil_ARMOR_v3.png"),optimize=True,compress_level=9)
make_armor_v3()

# V4 SIGNATURE — UV translation of the approved automotive concept.
def make_signature_v4():
    tex=gradient((72,82,90),(5,9,13))
    d=ImageDraw.Draw(tex,"RGB")
    cyan=(0,196,255); bright=(90,232,255); silver=(150,158,164); graphite=(22,28,34); black=(5,7,10)
    # hood / central signature: graphite field with two controlled blue blades
    d.polygon([(360,70),(512,45),(664,70),(610,355),(512,315),(414,355)],fill=graphite)
    d.line((418,92,486,338),fill=cyan,width=7)
    d.line((606,92,538,338),fill=cyan,width=7)
    # side architecture: silver upper body, black rocker, geometric rear armor
    for left in (True,False):
        if left:
            upper=[(55,175),(350,170),(405,385),(325,620),(65,560)]
            lower=[(60,555),(330,615),(400,810),(115,845),(55,760)]
            rear=[(205,610),(350,545),(420,650),(335,790),(245,735)]
        else:
            upper=[(969,175),(674,170),(619,385),(699,620),(959,560)]
            lower=[(964,555),(694,615),(624,810),(909,845),(969,760)]
            rear=[(819,610),(674,545),(604,650),(689,790),(779,735)]
        d.polygon(upper,fill=silver)
        d.polygon(lower,fill=black)
        d.polygon(rear,fill=graphite)
        # one deliberate energy line defines the body, with angular rear kick
        pts=[(upper[0][0],535),(upper[2][0],520),(rear[0][0],660),(rear[3][0],770)]
        d.line(pts,fill=cyan,width=7)
        d.line([(p[0],p[1]-7) for p in pts],fill=(20,70,90),width=2)
    # rear-quarter edition badge as geometry rather than text (Tesla render-safe)
    for cx in (270,754):
        d.polygon([(cx-28,665),(cx+18,645),(cx+28,680),(cx-18,700)],fill=(185,190,195))
        d.line((cx-8,652,cx-8,693),fill=cyan,width=3)
    # bumper accents and narrow cyan signature
    d.line((120,885,400,850),fill=cyan,width=5); d.line((624,850,904,885),fill=cyan,width=5)
    d.polygon([(420,870),(604,870),(580,935),(444,935)],fill=graphite)
    # mirror cyan cap detail
    d.line((138,385,180,385),fill=bright,width=4); d.line((844,385,886,385),fill=bright,width=4)
    out=Image.new("RGB",(W,H),(0,0,0))
    out.paste(tex,(0,0),mask)
    out.save(os.path.join(OUT,"JarvisMobil_SIGNATURE_v4.png"),optimize=True,compress_level=9)
make_signature_v4()
