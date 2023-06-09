#!/usr/bin/python3
# Create weather icon SVG files
# Copyright (C) 2023 Johanna Roedenbeck

"""
    This script is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This script is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""


import math
import optparse

WW_XML = '<?xml version="1.0" encoding="UTF-8" standalone="no"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"> '
WW_SVG1 = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%s" height="%s" viewBox="-64 -50 128 100"><g stroke-width="3">'
WW_SVG2 = '</g></svg>'

SUN_COLOR   = "#f6bc68"
MOON_COLOR  = "#da4935"
CLOUD_COLOR = "#828487"
RAIN_COLOR  = "#66a1ba"

def sonne(color=SUN_COLOR, fill="none"):
    """ sun icon """
    s = '<g stroke="%s">' % color
    s += '<circle cx="0" cy="0" r="18" fill="%s" />' % fill
    s += '<path d="'
    for i in range(8):
        w = math.pi*i/4
        ri = 24
        ro = 38
        s += 'M %s,%s L %s,%s ' % (round(math.cos(w)*ri,14),round(math.sin(w)*ri,14),round(math.cos(w)*ro,14),round(math.sin(w)*ro,14))
    s += '" />'
    s += '</g>'
    return s

def mond(x=0, y=-24, color=MOON_COLOR, fill="none"):
    """ moon icon """
    s = '<path stroke="%s" fill="%s" d="M %s,%s a 26,26 0 0 1 -22,39 a 24,24 0 1 0 22,-39 z" />' % (color,fill,x,y)
    return s

def wolke_grosz(x,y,offen=0,color=CLOUD_COLOR,fill="none"):
    """ cloud, large version """
    if fill!="none": offen = 0
    #s = '<path stroke="#828487" fill="none" d="M -27,12 h -4 a 20,20 0 0 1 0,-40 h 5 a 24,24 0 0 1 43,-9 h 2 a 16.25,16.25 0 0 1 15,10 a 20,20 0 0 1 -6.244997998398398,39 h -3 " />'
    s = '<path stroke="%s" fill="%s" d="M %s,%s '  % (color,fill,x,y)
    if offen: s += 'm %s,0 h %s ' % (offen,-offen)
    s += 'a 20,20 0 1 1 4.88026841,-39.3954371 a 24,24 0 0 1 43.20059379,-9.49083912 a 16.25,16.25 0 0 1 16.9191378,9.88627622 a 20,20 0 0 1 -6.244998,39'
    if offen: 
        s += 'h %s' % (-offen)
    else:
        s += 'z'
    s += '" />' 
    return s

def wolke_klein(x,y,color=CLOUD_COLOR,fill="none"):
    """ cloud, small version """
    s = '<path stroke="%s" stroke-width="1.8" fill="%s" d="M %s,%s a 12,12 0 1 1 2.92816105,-23.63726226 a 14.4,14.4 0 0 1 25.92035627,-5.69450347 a 9.75,9.75 0 0 1 10.15148268,5.93176573 a 12,12 0 0 1 -3.7469988,23.4 z " />' % (color,fill,x,y)
    return s

def wolke(x,y,scale=1.0,offen=0,color=CLOUD_COLOR,fill="none"):
    if fill!="none": offen = 0
    offen *= scale
    s = '<path stroke="%s" fill="%s" d="M %s,%s '  % (color,fill,x,y)
    if offen: s += 'm %s,0 h %s ' % (offen,-offen)
    s += 'a%s,%s 0 1 1 %s,%s ' % (20*scale,20*scale,4.88026841*scale,-39.3954371*scale)
    s += 'a%s,%s 0 0 1 %s,%s ' % (24*scale,24*scale,43.20059379*scale,-9.49083912*scale)
    s += 'a%s,%s 0 0 1 %s,%s ' % (16.25*scale,16.25*scale,16.9191378*scale,9.88627622*scale)
    s += 'a%s,%s 0 0 1 %s,%s ' % (20*scale,20*scale,-6.244998*scale,39*scale)
    if offen: 
        s += 'h %s' % (-offen)
    else:
        s += 'z'
    s += '" />' 
    return s

def blitz(x,y):
    """ lightning """
    #s= '<path stroke="none" fill="#f6bc68" d="M %s,%s l 7.93687345,-20.67626223 l -12.84686959,3.44230833 l 6.81974614,-17.76604611 h -4.30643568 l -5.54018777,20.67626223 l 12.68569967,-3.39912298 z" />' % (x,y)
    s= '<path stroke="none" fill="%s" d="M %s,%s l 8.03418996,-20.9297804 l -12.4943457,3.34784984 l 6.68617042,-17.41806944 h -5.42818409 l -4.83202054,20.9297804 l 12.02652853,-3.22249861 z" />' % (SUN_COLOR,x,y)
    return s

def regen(x=-28, y=10, v=30):
    """ rain """
    h = round(v*22/30,14)
    s = '<path stroke="none" fill="%s" d="M %s,%s ' % (RAIN_COLOR,x,y)
    for i in range(3):
        s += 'h 5 l %s,%s h -5 l %s,%s z ' % (h,v,-h,-v)
        if i<2: s += 'm 15,0 '
    s += '" />'
    return s
    
def niesel(x=-28,y=10,anzahl=5):
    """ drizzle """
    x += 1.5+22
    y += 30
    s = '<path stroke="%s" fille="none" stroke-dasharray="4 9" stroke-width="2" d="M %s,%s ' % (RAIN_COLOR,x,y)
    for i in range(anzahl):
        sign = 1 if i%2 else -1
        s += 'l %s,%s ' % (22*sign,30*sign)
        if i<4: s += 'm 7.5,0 '
    s += '" />'
    return s

def schneeflocke(x, y, r, innen=True):
    """ snowflake """
    y -= r
    s = '<path stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none" d="M %s,%s ' % (RAIN_COLOR,r*0.15,x,y)
    for i in range(3):
        phi = i*math.pi/3
        if i>0:
            s += 'm%s,%s ' % (round(-xa-r*math.sin(phi),8),round(-ya-r*math.cos(phi),8))
        s += 'l%s,%s ' % (round(2*r*math.sin(phi),8),round(2*r*math.cos(phi),8))
        xa,ya = r*math.sin(phi),r*math.cos(phi)
    for i in range(6):
        phi = i*math.pi/3
        x,y = -r*math.sin(phi),-r*math.cos(phi)
        s += 'm%s,%s ' % (round(x-xa,8),round(y-ya,8))
        r2 = r/3
        s += 'm%s,%s ' % (round(r2*math.sin(phi+math.pi/3),8),round(r2*math.cos(phi+math.pi/3),8))
        s += 'l%s,%s ' % (round(r2*math.sin(phi+5*math.pi/3),8),round(r2*math.cos(phi+5*math.pi/3),8))
        s += 'l%s,%s ' % (round(r2*math.sin(phi-2*math.pi/3),8),round(r2*math.cos(phi-2*math.pi/3),8))
        s += 'm%s,%s ' % (round(r2*math.sin(phi+2*math.pi/3),8),round(r2*math.cos(phi+2*math.pi/3),8))
        xa,ya = x,y
    if innen:
        for i in range(6):
            phi = i*math.pi/3
            x,y = -r*1.5/3*math.sin(phi),-r*1.5/3*math.cos(phi)
            s += 'm %s,%s ' % (round(x-xa,8),round(y-ya,8))
            r2 = r/6
            s += 'm%s,%s ' % (round(r2*math.sin(phi+math.pi/3),8),round(r2*math.cos(phi+math.pi/3),8))
            s += 'l%s,%s ' % (round(r2*math.sin(phi+5*math.pi/3),8),round(r2*math.cos(phi+5*math.pi/3),8))
            s += 'l%s,%s ' % (round(r2*math.sin(phi-2*math.pi/3),8),round(r2*math.cos(phi-2*math.pi/3),8))
            s += 'm%s,%s ' % (round(r2*math.sin(phi+2*math.pi/3),8),round(r2*math.cos(phi+2*math.pi/3),8))
            xa,ya = x,y
    s += '" />'
    return s

def regentropfen(x, y, r):
    """ raindrop """
    r *= (1+0.15/2)
    r1 = 5*r
    r2 = 0.6*r
    s = '<path stroke="none" fill="%s" d="M%s,%s ' % (RAIN_COLOR,x,y-r)
    s += 'a%s,%s 0 0 1 %s,%s ' % (r1,r1,-0.508568808*r,1.081632653*r)
    s += 'a%s,%s 0 1 0 %s,0 ' % (r2,r2,1.017137616*r)
    s += 'a%s,%s 0 0 1 %s,%s z" />' % (r1,r1,-0.508568808*r,-1.081632653*r)
    return s
    
def schlitterlinie(x, y):
    s = '<path stroke="none" fill="#000000" d="M%s,%s l8.54455967,-4.047423 ' % (x-14.02235138,y)
    # left
    s += 'a6.04100450,6.04100450 0 0 0 2.54603347,-8.64621208 l-3.23725145,-5.21347156 a2.74580363,2.74580363 0 0 1 0.78256116,-3.71485342 l4.93895246,-3.37803994 h-1.38888889 '
    s += 'l-5.10795449,2.93585208 a4.68254091,4.68254091 0 0 0 -2.09563466,5.5796135 l2.27226862,6.62156404 a3.29583971,3.29583971 0 0 1 -1.84474537,4.10998876 l-13.74323385,5.75298161 z '
    # right
    s += 'm33.33333333,0 l1.22771241,-1.22771241 a6.20359314,6.20359314 0 0 0 -1.28480621,-9.75907203 l-13.55967183,-7.82868018 a3.22628070,3.22628070 0 0 1 -1.41857181,-3.89749403 l0.83241498,-2.28704135 h-1.38888889 '
    s += 'l-0.68119443,1.08342259 a4.68254091,4.68254091 0 0 0 1.30173924,6.30605466 l12.49300857,8.59055233 a2.68888799,2.68888799 0 0 1 0.13365758,4.33313596 l-5.98873292,4.68683446 z'
    s += '" />' 
    return s
    

def snowflake_icon_15px():
    s = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="15px" height="15px" viewBox="-7.5 -7.5 15 15">'
    s += schneeflocke(0,0,6.95,False)
    s += '</svg>'
    return s
    
def raindrop_icon_15px():
    s = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="15px" height="15px" viewBox="-7.5 -7.5 15 15">'
    s += regentropfen(0,0,6.95)
    s += '</svg>'
    return s
    
def wetterleuchten(gefuellt=False):
    """ lightning, thunderstorm without precipitation """
    s = wolke_grosz(-31,28,fill=CLOUD_COLOR if gefuellt else "none")
    s += blitz(-4,16)
    return s

def wetterleuchten2(gefuellt=False):
    """ lightning, thunderstorm without precipitation, another design """
    s = wolke_klein(-20,0,fill=CLOUD_COLOR if gefuellt else "none")
    s += blitz(-4,38)
    return s

def gewitter(gefuellt=False):
    """ thunderstorm with rain """
    s = wolke_grosz(-31,22,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += blitz(-4,6)
    s += regen()
    return s

def hagelgewitter(gefuellt=False):
    """ thunderstorm with hail """
    s = wolke_grosz(-31,16 if gefuellt else 22,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += blitz(-4,6)
    s += '<g stroke="none" fill="%s">' % RAIN_COLOR
    s += '<circle cx="-15" cy="%s" r="4" />' % (42 if gefuellt else 37)
    s += '<circle cx="-6" cy="%s" r="4" />' % (25 if gefuellt else 19)
    s += '<circle cx="11" cy="%s" r="4" />' % (36 if gefuellt else 30)
    s += '</g>'
    return s

def regen_gesamt(gefuellt=False):
    """ rain """
    s = wolke_grosz(-31,22,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += regen()
    return s

def niesel_gesamt(gefuellt=False):
    """ drizzle """
    s = wolke_grosz(-31,22,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += niesel()
    return s

def schneefall(gefuellt=False,innen=True):
    """ snow """
    s = wolke_grosz(-31,22,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += schneeflocke(-13,17,10,innen)
    s += schneeflocke(12,10,10,innen)
    s += schneeflocke(5,33,10,innen)
    return s

def schneeregen(gefuellt=False,innen=True):
    """ sleet """
    s = wolke_grosz(-31,22,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += schneeflocke(-13,33,10,innen)
    s += niesel(-10,10,3)
    return s

def hagel(gefuellt=False):
    """ hail """
    s = wolke_grosz(-31,22,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += '<g stroke="none" fill="%s">' % RAIN_COLOR
    s += '<circle cx="-15" cy="37" r="4" />'
    s += '<circle cx="-6" cy="19" r="4" />'
    s += '<circle cx="11" cy="30" r="4" />'
    s += '</g>'
    return s

def glatt(gefuellt=False):
    s = schlitterlinie(10.6,45)
    s += schneeflocke(-23,32.5,10,innen=False)
    return s

def gefrierender_regen(gefuellt=False,innen=False):
    """ freezing rain (slithering line below the cloud) """
    scale = 0.85
    s = wolke(-31*scale,4,scale=scale,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += regen(-27,-7,30*scale)
    s += schlitterlinie(4.6,48)
    s += schneeflocke(-17,34,8,innen=innen)
    return s
    
def gefrierender_regen2(gefuellt=False,innen=False):
    """ freezing rain (slithering line within the cloud) """
    s = wolke_grosz(-31,22,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += regen()
    s += schlitterlinie(10.6,5)
    s += schneeflocke(-15,-7,8,innen=innen)
    return s

'''
def gefrierender_regen(gefuellt=False,innen=False):
    """ freezing rain """
    s = wolke(-31+21,22-14,scale=0.85,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += regen(-28+17,10-14,30*0.85)
    b = 74
    h = b*0.5
    v = round(b*math.sin(60*math.pi/180),8)
    s += '<path stroke="none" fill="#F0F0F0" d="M-60,46 l%s,%s l%s,%s z" />' % (h,-v,h,v)
    b = 68
    h = b*0.5
    v = round(b*math.sin(60*math.pi/180),8)
    s += '<path stroke="#FF0000" stroke-width="6" stroke-linecap="round" fill="none" d="M-56,42 l%s,%s l%s,%s z" />' % (h,-v,h,v)
    s += schlitterlinie(-23,37)
    return s
'''

def gefrierender_regen4(gefuellt=False,innen=False):
    """ freezing rain (traffic sign like) """
    #s = wolke(-31+21,22-14,scale=0.85,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    #s += regen(-28+17,10-14,30*0.85)
    s = wolke_grosz(-31-7,22-7,offen=4,fill=CLOUD_COLOR if gefuellt else "none")
    s += regen(-28-7,10-7,30)
    b = 42
    h = b*0.5
    v = round(b*math.sin(60*math.pi/180),8)
    #s += '<path stroke="none" fill="#F0F0F0" d="M-60,46 l%s,%s l%s,%s z" />' % (h,-v,h,v)
    s += '<path stroke="#F0F0F0" stroke-width="8" stroke-linejoin="round" fill="#F0F0F0" d="M10,42 l%s,%s l%s,%s z" />' % (h,-v,h,v)
    b = 42
    h = b*0.5
    v = round(b*math.sin(60*math.pi/180),8)
    #s += '<path stroke="#FF0000" stroke-width="6" stroke-linecap="round" fill="none" d="M-56,42 l%s,%s l%s,%s z" />' % (h,-v,h,v)
    s += '<path stroke="#b52126" stroke-width="6" stroke-linejoin="round" fill="none" d="M10,42 l%s,%s l%s,%s z" />' % (h,-v,h,v)
    s += '<g transform="scale(0.5)">'
    #s += schlitterlinie(-23*2-25,37*2)
    s += schlitterlinie(23*2+15,37*2)
    s += '</g>'
    return s

def unknown(color=CLOUD_COLOR):
    """ unknown weather or no data """
    s = wolke_grosz(-31,28,color=color)
    s += '<text x="-18" y="18" fill="%s" style="font-family:sans-serif;font-size:50px;font-weight:normal;text-align:center">?</text>' % color
    return s

def bewoelkt(wolke=1,mit_sonne=False,mit_mond=False,gefuellt=False):
    """ cloudiness
    
        wolke = 0 --> sun or moon
                1 --> sun or moon and small cloud
                2 --> sun or moon and cloud
                3 --> sun or moon and 2 clouds
                4 --> 2 clouds
        mit_sonne = True for day icons
        mit_mond = True for night icons
    """
    if wolke==0:
        # clear day or night
        if mit_sonne:
            return sonne(fill=SUN_COLOR if gefuellt else "none")
        if mit_mond:
            return mond(fill=MOON_COLOR if gefuellt else "none")
    s = ""
    xy = (-31,28)
    if mit_sonne and wolke<4:
        if wolke==3:
            # sun circle
            cx = -28
            cy = -12
            r = 14
            # sun beams
            ri = 19
            ro = 30
            #arc = (-20,-23.49,0,-41.72,-9.02)
            arc = (-19.99475974,-23.48547467,0,-41.65782625,-8.92367394)
            strahlen = (4,5,6)
        elif wolke==2:
            # sun circle
            cx = -32
            cy = -18
            r = 14
            # sun beams
            ri = 19
            ro = 30
            #arc = (-18,-17.87,1,-39.28,-6.04)
            arc = (-18.00252351,-17.73419552,1,-39.25615559,-6.02718888)
            strahlen = (3,4,5,6,7)
            xy = (-25,28)
        else:
            cx = 0
            cy = -7
            r = 18
            ri = 24
            ro = 38
            #arc = (17.39,-2.45,1,-5.29,10.24)
            arc = (17.40699560,-2.41780574,1,-5.26007294,10.21428571)
            strahlen = (3,4,5,6,7,0)
        s += '<g stroke="%s">' % SUN_COLOR
        if not arc or gefuellt:
            s += '<circle cx="%s" cy="%s" r="%s" fill="%s" />' % (cx,cy,r,SUN_COLOR if gefuellt else "none")
        s += '<path fill="none" d="'
        if arc:
            s += 'M %s,%s A %s,%s 0 %s 0 %s,%s ' % (arc[0:2]+(r,r)+arc[2:])
        for i in range(8):
            w = math.pi*i/4
            if i in strahlen:
                s += 'M %s,%s L %s,%s ' % (round(math.cos(w)*ri,14)+cx,round(math.sin(w)*ri,14)+cy,round(math.cos(w)*ro,14)+cx,round(math.sin(w)*ro,14)+cy)
        s += '" />'
        s += '</g>'
    if mit_mond and wolke<4:
        if wolke==1:
            if gefuellt:
                s += mond(fill=MOON_COLOR if gefuellt else "none")
            else:
                s += '<path stroke="%s" fill="none" d="M 19.97705974,-2.12865019 a 24,24 0 0 0 -19.97705974,-28.87134981 a 26,26 0 0 1 -22,39 a 24,24 0 0 0 11.27165715,7.62388061" />' % MOON_COLOR
        elif wolke>=2:
            #s += '<path stroke="#da4935" fill="none" d="M -34,-43 a 26,26 0 0 1 -22,39 a 24,24 0 1 0 22,-39 z" />'
            if gefuellt:
                s += mond(-34,-43,fill=MOON_COLOR if gefuellt else "none")
            else:
                s += '<path stroke="%s" fill="none" d="M -13.88,-23.64 a 24,24 0 0 0 -20.12,-19.36 a 26,26 0 0 1 -22,39 a 24,24 0 0 0 11.44,7.68 m 30.68,-27.32 a 24,24 0 0 0 -20.12,-19.36 " />' % MOON_COLOR
            xy = (-25,28)
    if wolke>=3:
        # mostly cloudy day or night or overcast
        w3 = (5,-30)
        if mit_mond and wolke==3: w3 = (11,-30)
        if gefuellt:
            s += wolke_klein(w3[0]+5,w3[1]+20,fill="#A2A4A7" if gefuellt else "none")
        else:
            s += '<path stroke="%s" stroke-width="1.8" fill="none" d="M %s,%s a 14.4,14.4 0 0 1 25.8,-5.4 h 2 a 9.75,9.75 0 0 1 9,6 a 12,12 0 0 1 0.3,22.68" />' % (CLOUD_COLOR,w3[0],w3[1])
    if wolke==1:
        # mostly clear day or night --> small cloud
        #s += '<path stroke="#828487" stroke-width="1.8" fill="none" d="M 0,33 a 12,12 0 1 1 2.92816105,-23.63726226 a 14.4,14.4 0 0 1 25.92035627,-5.69450347 a 9.75,9.75 0 0 1 10.15148268,5.93176573 a 12,12 0 0 1 -3.7469988,23.4 z " />' 
        s += wolke_klein(0,33,fill="#A2A4A7" if gefuellt else "none")
    if wolke>=2:
        # large cloud
        ##s += '<path stroke="#828487" fill="none" d="M %s,%s a 20,20 0 0 1 0,-40 h 5 a 24,24 0 0 1 43,-9 h 2 a 16.25,16.25 0 0 1 15,10 a 20,20 0 0 1 -6.244997998398398,39 z " />' % xy
        ##s += '<path stroke="#828487" fill="none" d="M %s,%s a 20,20 0 1 1 4.88026841,-39.3954371 a 24,24 0 0 1 43.20059379,-9.49083912 a 16.25,16.25 0 0 1 16.9191378,9.88627622 a 20,20 0 0 1 -6.244998,39 z " />' % xy
        s += wolke_grosz(xy[0],xy[1],fill=CLOUD_COLOR if gefuellt else "none")
    return s

def nebel():
    """ fog """
    s = '<path stroke="rgba(111,155,164,90)" stroke-linecap="round" d="'
    for i in range(4):
        s += 'M -39,%s h 78 ' % (10*i-15)
    s += '" />'
    return s

def wind():
    """ wind """
    s = '<path stroke-width="6" stroke="#404040" fill="none" d="M-45,-15 h40 a12,12 0 1 0 -12,-12 M-45,0 h75 a12,12 0 1 0 -12,-12 M-45,15 h57.5 a12,12 0 1 1 -12,12" />'
    return s

def tornado():
    """ tornado, funnel clouds """
    # TODO
    return ""
  

# icons of cloudiness
N_ICON_LIST = [
    (0,True,False,'clear-day'),
    (0,False,True,'clear-night'),
    (1,True,False,'mostly-clear-day'),
    (1,False,True,'mostly-clear-night'),
    (2,True,False,'partly-cloudy-day'),
    (2,False,True,'partly-cloudy-night'),
    (3,True,False,'mostly-cloudy-day'),
    (3,False,True,'mostly-cloudy-night'),
    (4,True,False,'cloudy'),
    (4,False,True,'cloudy-night')
]

# icons of present weather
ICON_WW = {
   9:'SVG_ICON_WIND',
  11:'SVG_ICON_FOG',
  12:'SVG_ICON_FOG',
  13:'SVG_ICON_LIGHTNING',
  # 14...16: distant weather
  17:'SVG_ICON_LIGHTNING',
  18:'SVG_ICON_WIND',
  19:"'"+tornado()+"'",
  # 20...29: finished weather
  # 30...39: wind
  # 40...49: mist and fog
  50:'SVG_ICON_DRIZZLE',
  51:'SVG_ICON_DRIZZLE',
  52:'SVG_ICON_DRIZZLE',
  53:'SVG_ICON_DRIZZLE',
  54:'SVG_ICON_DRIZZLE',
  55:'SVG_ICON_DRIZZLE',
  56:'SVG_ICON_FREEZINGRAIN',
  57:'SVG_ICON_FREEZINGRAIN',
  58:'SVG_ICON_RAIN',
  59:'SVG_ICON_RAIN',
  60:'SVG_ICON_RAIN',
  61:'SVG_ICON_RAIN',
  62:'SVG_ICON_RAIN',
  63:'SVG_ICON_RAIN',
  64:'SVG_ICON_RAIN',
  65:'SVG_ICON_RAIN',
  66:'SVG_ICON_FREEZINGRAIN',
  67:'SVG_ICON_FREEZINGRAIN',
  68:'SVG_ICON_SLEET',
  69:'SVG_ICON_SLEET',
  70:'SVG_ICON_SNOW',
  71:'SVG_ICON_SNOW',
  72:'SVG_ICON_SNOW',
  73:'SVG_ICON_SNOW',
  74:'SVG_ICON_SNOW',
  75:'SVG_ICON_SNOW',
  77:'SVG_ICON_SNOW',
  78:'SVG_ICON_SNOW',
  79:'SVG_ICON_HAIL',
  80:'SVG_ICON_RAIN',
  81:'SVG_ICON_RAIN',
  82:'SVG_ICON_RAIN',
  83:'SVG_ICON_SLEET',
  84:'SVG_ICON_SLEET',
  85:'SVG_ICON_SNOW',
  86:'SVG_ICON_SNOW',
  87:'SVG_ICON_HAIL',
  88:'SVG_ICON_HAIL',
  89:'SVG_ICON_HAIL',
  90:'SVG_ICON_HAIL',
  91:'SVG_ICON_RAIN',
  92:'SVG_ICON_RAIN',
  93:'SVG_ICON_SNOW',
  94:'SVG_ICON_SNOW',
  95:"'"+gewitter()+"'",
  96:"'"+hagelgewitter()+"'",
  97:"'"+gewitter()+"'",
  98:'SVG_ICON_LIGHTNING',
  99:"'"+hagelgewitter()+"'"
}

if True:

    usage = "Usage: %prog [options]"
    epilog = None

    # Create a command line parser:
    parser = optparse.OptionParser(usage=usage, epilog=epilog)

    # options
    parser.add_option("--write-svg", dest="writesvg", action="store_true",
                      default=False,
                      help="write SVG files")
    parser.add_option("--write-py", dest="writepy", action="store_true",
                      default=False,
                      help="write Python script")
    parser.add_option("--filled", action="store_true",
                      default=False,
                      help="filled icons")

    (options, args) = parser.parse_args()


if options.writesvg:

    gefuellt = options.filled
    WW_ICON_LIST = [
        ('unknown',unknown()),
        ('fog',nebel()),
        ('lightning',wetterleuchten2(gefuellt)),
        ('lightning2',wetterleuchten(gefuellt)),
        ('thunderstorm',gewitter(gefuellt)),
        ('thunderstorm-hail',hagelgewitter(gefuellt)),
        ('rain',regen_gesamt(gefuellt)),
        ('drizzle',niesel_gesamt(gefuellt)),
        ('snowflake',schneeflocke(0,0,40,False)),
        ('snowflake2',schneeflocke(0,0,40,True)),
        ('raindrop',regentropfen(0,0,40)),
        ('snow',schneefall(gefuellt=gefuellt,innen=False)),
        ('snow2',schneefall(gefuellt=gefuellt,innen=True)),
        ('sleet',schneeregen(gefuellt=gefuellt,innen=False)),
        ('hail',hagel(gefuellt)),
        ('wind',wind()),
        ('freezingrain',gefrierender_regen(gefuellt=gefuellt,innen=False)),
        ('freezingrain2',gefrierender_regen4(gefuellt=gefuellt,innen=False))
    ]
    for idx,val in enumerate(N_ICON_LIST):
        s = bewoelkt(val[0],val[1],val[2],gefuellt=gefuellt)
        with open(val[3]+'.svg','w') as file:
            file.write(WW_XML)
            file.write(WW_SVG1 % (128,100))
            file.write(s)
            file.write(WW_SVG2)
    for idx,val in enumerate(WW_ICON_LIST):
        with open(val[0]+'.svg','w') as file:
            file.write(WW_XML)
            file.write(WW_SVG1 % (128,100))
            file.write(val[1])
            file.write(WW_SVG2)
    with open('snowflake-icon-15px.svg','w') as file:
        file.write(snowflake_icon_15px())
    with open('raindrop-icon-15px.svg','w') as file:
        file.write(raindrop_icon_15px())


if options.writepy:

    s =  "SVG_ICON_START = '%s'\n" % WW_SVG1
    s += "SVG_ICON_END = '%s'\n" % WW_SVG2
    s += "SVG_ICON_UNKNOWN = '%s'\n" % unknown()
    s += "SVG_ICON_CLOUDY = '%s'\n" % bewoelkt(4,gefuellt=options.filled)
    s += "SVG_ICON_FOG = '%s'\n" % nebel()
    s += "SVG_ICON_WIND = '%s'\n" % wind()
    s += "SVG_ICON_RAIN = '%s'\n" % regen_gesamt(gefuellt=options.filled)
    s += "SVG_ICON_DRIZZLE = '%s'\n" % niesel_gesamt(gefuellt=options.filled)
    s += "SVG_ICON_HAIL = '%s'\n" % hagel(gefuellt=options.filled)
    s += "SVG_ICON_SLEET = '%s'\n" % schneeregen(gefuellt=options.filled)
    s += "SVG_ICON_SNOW = '%s'\n" % schneefall(gefuellt=options.filled)
    s += "SVG_ICON_FREEZINGRAIN = '%s'\n" % gefrierender_regen(gefuellt=options.filled)
    s += "SVG_ICON_LIGHTNING = '%s'\n" % wetterleuchten(gefuellt=options.filled)
    s += "SVG_ICON_N = [\n"
    for idx,val in enumerate(N_ICON_LIST):
        if idx==4: break
        if val[1]:
            s += "    ('"
        else:
            s += "     '"
        s += bewoelkt(val[0],val[1],val[2],gefuellt=options.filled)
        if val[2]:
            s += "'),"
        else:
            s += "',"
        s += '\n'
    s += "    (SVG_ICON_CLOUDY,SVG_ICON_CLOUDY),\n"
    s += "    (SVG_ICON_FOG,SVG_ICON_FOG),\n"
    s += "    (SVG_ICON_UNKNOWN,SVG_ICON_UNKNOWN)\n"
    s += ']\n\n'
    s += 'def svg_icon_n(okta, night=False, width=128):\n'
    s += '    try:\n'
    s += '        height = width * 0.78125\n'
    s += '        night = 1 if night else 0\n'
    s += '        idx = (0,1,1,2,2,2,3,3,4,5,6)[okta]\n'
    s += '        return ((SVG_ICON_START % (width,height))+\n'
    s += '            SVG_ICON_N[idx][night]+\n'
    s += '            SVG_ICON_END)\n'
    s += '    except (ArithmeticError,LookupError,TypeError,ValuError):\n'
    s += '        return ""\n\n'
    s += 'SVG_ICON_WW = [\n'
    for idx in range(100):
        if idx<20 or idx>=50:
            if idx in ICON_WW:
                s += "    # %02d\n    %s,\n" % (idx,ICON_WW[idx])
            else:
                s += '    # %02d\n    None,\n' % idx
        elif idx<30:
            s += '    # %02d\n    None,\n' % idx
        elif idx<40:
            s += '    # %02d\n    SVG_ICON_WIND,\n' % idx
        else:
            s += '    # %02d\n    SVG_ICON_FOG,\n' % idx
    s += ']\n\n'
    s += 'def svg_icon_ww(ww, width=128):\n'
    s += '    try:\n'
    s += '        height = width * 0.78125\n'
    s += '        return ((SVG_ICON_START % (width,height))+\n'
    s += '            SVG_ICON_WW[ww]+\n'
    s += '            SVG_ICON_END)\n'
    s += '    except (ArithmeticError,LookupError,TypeError,ValuError):\n'
    s += '        return ""\n\n'
    print(s)
