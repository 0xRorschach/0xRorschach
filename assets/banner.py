# Banner v2: ham mürekkep görseli (OpenAI image gen, yazısız) + kodla dizilen yazı
from PIL import Image, ImageDraw, ImageFont
im=Image.open('assets/blot-sb.png').convert('RGB')
W=1600; im=im.resize((W,int(im.height*W/im.width)),Image.LANCZOS)
dr=ImageDraw.Draw(im)
INK=(12,12,12); SOFT=(70,70,70); RED=(12,12,12)
it=ImageFont.truetype('assets/SourceSerif4-Italic.ttf',68)
mono=ImageFont.truetype('assets/IBMPlexMono-Regular.ttf',21)
x=72; y=im.height//2-60
dr.text((x,y),'Rorschach',font=it,fill=INK)
def spaced(xy,s,font,fill,gap=4):
    x0,y0=xy
    for ch in s:
        dr.text((x0,y0),ch,font=font,fill=fill); x0+=dr.textlength(ch,font=font)+gap
spaced((x+3,y+100),'PLATE I',mono,SOFT)
dr.line([(x+3,y+136),(x+36,y+136)],fill=RED,width=2)
spaced((x+3,y+150),'@0x_Rorschach',mono,SOFT,gap=2)
im.save('assets/banner.png',optimize=True); print(im.size)
