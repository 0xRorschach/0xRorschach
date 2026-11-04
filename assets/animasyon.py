# Plate I hareketli: mürekkep katlama ekseninden dışa doğru kâğıda yayılır, sonra durağan banner'da kalır.
import numpy as np
from PIL import Image, ImageFilter
W,H=1200,600; FPS=20
son=Image.open('assets/banner.png').convert('RGB').resize((W,H),Image.LANCZOS)
ham=Image.open('assets/blot-sb.png').convert('RGB').resize((W,H),Image.LANCZOS)
O=np.asarray(son).astype(float); R=np.asarray(ham).astype(float)
# kâğıt tahmini: ham görselde mürekkebi büyük maksimum filtreyle sil
# boş kâğıt: aynı görselin mürekkepsiz hâli (image edit); doku ve ışık birebir olduğundan maske sınırı görünmez
P=np.asarray(Image.open('assets/kagit-sb.png').convert('RGB').resize((W,H),Image.LANCZOS)).astype(float)
yazi=(np.abs(O-R).sum(axis=2)>40)  # yalnız kodla dizilen yazı pikselleri
eksen=int(1120*W/1774)
y,x=np.mgrid[0:H,0:W].astype(float)
rng=np.random.default_rng(3)
def gur(sc):
    n=rng.random((H//sc+2,W//sc+2));im=Image.fromarray((n*255).astype('uint8')).resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(sc*0.7));a=np.asarray(im).astype(float);return (a-a.min())/(a.max()-a.min()+1e-9)
g=gur(40)*0.6+gur(12)*0.3+gur(4)*0.1
g=(g+g[:, ::-1])/2  # simetrik gürültü
alan=np.sqrt(((x-eksen)/(W*0.52))**2+((y-H*0.42)/(H*0.95))**2)+0.38*(g-0.5)
# koyu çekirdek önce, soluk hale en son gelsin
Lr=R@[0.299,0.587,0.114]; Lb=P@[0.299,0.587,0.114]
koyu=np.clip((Lb-Lr)/90,0,1)
alan=alan+0.22*(1-koyu)
alan=(alan-alan.min())/(alan.max()-alan.min())+0.02
def kare(t):
    # t: 0..1 yayılma; yumuşak cephe
    a=np.clip((t*1.12-alan)/0.10,0,1)
    a=a*a*(3-2*a)
    # soluk hale ve gölge: uzamsal cephe yerine bütün olarak yavaşça belirsin (düz sınır oluşmaz)
    w=np.clip(koyu/0.35,0,1); w=w*w*(3-2*w)
    a=w*a+(1-w)*(t**1.6)
    F=P*(1-a[...,None])+R*a[...,None]
    # ıslak cephe: yeni gelen mürekkep bir an koyu
    c=np.exp(-((t*1.12-alan-0.05)/0.05)**2)*0.18*(t<1)
    F=F*(1-c[...,None])
    F[yazi]=O[yazi]
    return F
kareler=[]
# 0.4 sn boş kâğıt + kat çizgisi, 2.6 sn yayılma (yavaşlayan), 2 sn bekleme
for i in range(int(0.4*FPS)): kareler.append(kare(0.0))
n=int(2.6*FPS)
for i in range(n):
    s=(i+1)/n; t=s*s*(3-2*s)
    kareler.append(kare(t))
kareler=[Image.fromarray(np.clip(f,0,255).astype('uint8')) for f in kareler]
# son kare = durağan banner (yazı alanı dahil birebir)
kareler.append(son); 
sure=[int(1000/FPS)]*(len(kareler)-1)+[2500]
kareler[0].save('assets/banner-hareketli.webp',save_all=True,append_images=kareler[1:],duration=sure,loop=1,quality=82,method=6)
kareler[0].save('/opt/data/cache/scratch/k0.png'); kareler[len(kareler)//3].save('/opt/data/cache/scratch/k1.png'); kareler[len(kareler)*2//3].save('/opt/data/cache/scratch/k2.png')
import os;print(len(kareler),os.path.getsize('assets/banner-hareketli.webp')//1024,'KB')
