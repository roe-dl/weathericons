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

# Schild an einem Kasten in der Nähe: 144 x 186 mm

import math
import optparse

WIDTH = 148
HEIGHT = 210
BORDER1 = 1
BORDER2 = 7

SIGNAL_RED = "#a92121"
SIGNAL_WHITE = "#ecece7"

WW_XML = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
WW_SVG1 = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%s%s" height="%s%s" viewBox="0 0 %s %s">\n'
WW_SVG_G = '  <g stroke-width="2">\n'
WW_SVG2 = '  </g>\n</svg>\n'

epfeil_coordinates = (
    (-0.1682952122,0.5728820612),
    (0.2461538364,-0.1269230985),
    (-0.0526681452,0.3855718688),
    (-0.050322184,-0.0734997543),
    (0.0387837266,0.2417740425),
    (0.1411296744,-0.2038461369),
    (-0.0714760171,0.0444421877),
    (0.1483991222,-0.5463653028),
    (-0.2653846543,0.1461538497),
    (0.1942307946,-0.4403845977),
    (-0.1605509414,0.0001949137),
)

def matrix(i,pers):
    return (
        #i[0]*math.cos(pers)-i[1]*math.sin(pers),
        i[0],
        -i[0]*math.sin(pers)+i[1]
    )

def epfeil(x=0, y=0, factor=1, color='currentColor',pers=0):
    s = '    <path stroke="none" fill="%s" d="' % color
    j = matrix((-0.013652021551523648,-1.0),pers)
    s += 'M%s,%s ' % (round(x+j[0]*factor,3),round(y+j[1]*factor,3))
    for i in epfeil_coordinates:
        j = matrix(i,pers)
        s += 'l%s,%s ' % (round(j[0]*factor,6),round(j[1]*factor,6))
    s += 'Z" />\n'
    return s

def rand(x,y,b,h,r,color):
    """ symbol border """
    br = b-2*r
    hr = h-2*r
    return '''    <path
     fill="%s" stroke="none"
     d="M%s,%s h%s v%s h%s v%s h%s v%s h%s v%s h%s v%s h%s z" />
''' % (color,x+0.5*b,y,0.5*b,h,-b,-h,0.5*b,r,-0.5*br,hr,br,-hr,-0.5*br)

def sonne(x,y,r,color='currentColor'):
    border = BORDER2-0.2
    x2 = round(math.sqrt(r*r-border*border),6)
    s = '''    <path
      fill="none" stroke="%s" stroke-width="1.5"
      d="M%s,%s a33,33 0 0 1 %s,%s" />
''' % (color,round(x,3),round(y+r,3),round(-x2,3),round(border-r,3))
    s += '    <path\n       fill="none" stroke="%s" stroke-linecap="round" stroke-width="1"\n       d="' % color
    for w in range(7):
        if w&1:
            strahl = 18
        else:
            strahl = 12
        gap = 4
        ww = (95.625+11.25*w)*math.pi/180
        x1 = round(x+(r+gap)*math.cos(ww),3)
        x2 = round(x+(r+gap+strahl)*math.cos(ww),3)
        y1 = round(y+(r+gap)*math.sin(ww),3)
        y2 = round(y+(r+gap+strahl)*math.sin(ww),3)
        s += 'M%s,%s L%s,%s ' % (x1,y1,x2,y2)
    s += '" />\n'
    return s

def haus(x,y,battery,color='currentColor'):
    b = 74    # Breite Stirnseite
    h1 = 47   # Höhe bis Dachanfang
    h2 = 110  # Gesamthöhe
    p = 42    # Länge Seitenwand in x-Richtung
    ex = 338  # Fluchtpunkt x
    ey = 227  # Fluchtpunkt y
    # back wall of the house
    yu = p/(ex-b)*ey
    ym = p/(ex-b)*(ey-h1)+h1
    yo = p/(ex-b/2)*(ey-h2)+h2
    # vertical line in the middle of the roof
    cc_m = (p*0.5+b,ym*0.5+h1*0.5,p*0.5+0.5*b,(yo-h2)*0.5+h2)
    # end point of the middle wire
    vv = 0.065
    coord_m = ((cc_m[2]-cc_m[0])*vv+cc_m[0],(cc_m[3]-cc_m[1])*vv+cc_m[1])
    # PV panels and wires on the roof
    s1 = ''
    s2 = ''
    s3 = ''
    for i in range(4):
        # längs
        hori = [0.1,0.475] if i&1 else [0.525,0.9]
        hori.append(0.5*sum(hori))
        if i==3 or i==2:
            hori.append(0.5)
        # hoch
        vert = (0.12,0.475) if i&2 else (0.525,0.88)
        # edges of the panel
        coord = []
        for cc in ((p*hh+b,ym*hh+h1*(1-hh),p*hh+0.5*b,(yo-h2)*hh+h2) for hh in hori):
            #print('cc',cc)
            for vv in vert:
                coord.append(((cc[2]-cc[0])*vv+cc[0],(cc[3]-cc[1])*vv+cc[1]))
        #print(coord)
        # panel including filled area
        s1 += 'M%s,%s ' % (round(x+coord[0][0],3),round(y-coord[0][1],3))
        for j in ((0,2),(2,3),(3,1)):
            s1 += 'l%s,%s ' % (
                round(coord[j[1]][0]-coord[j[0]][0],3),
                round(coord[j[0]][1]-coord[j[1]][1],3)
            )
        s1 += 'z '
        # wire
        d_wire = (-0.15*(coord[5][0]-coord[4][0]),-0.15*(coord[4][1]-coord[5][1]))
        s2 += 'M%s,%s l%s,%s ' % (
            round(x+coord[4][0],3),round(y-coord[4][1],3),
            round(d_wire[0],3),round(d_wire[1],3)
        )
        if i==3 or i==2:
            d_wire_m = (-0.15*(coord[7][0]-coord[6][0]),-0.15*(coord[6][1]-coord[7][1]))
            #print(coord[6][0]+d_wire_m[0],coord[6][1]+d_wire_m[1],coord[4][0]+d_wire[0],coord[4][1]+d_wire[1])
            #s2 += 'l%s,%s ' % (coord[6][0]+d_wire_m[0]-d_wire[0]-coord[4][0],-coord[6][1]-d_wire_m[1]+d_wire[1]+coord[4][1])
            s2 += 'L%s,%s ' % (round(x+coord[6][0]+d_wire_m[0],3),round(y-coord[6][1]+d_wire_m[1],3))
            #print( '%s,%s ' % (coord[6][0]+d_wire_m[0]-d_wire[0]-coord[4][0],-coord[6][1]-d_wire_m[1]+d_wire[1]+coord[4][1]))
            #s2 += 'l%s,%s ' % (coord_m[0]-d_wire[0]-coord[4][0],-coord_m[1]-d_wire[1]+coord[4][1])
        # panel width and height
        bottom = (coord[2][0]-coord[0][0],coord[2][1]-coord[0][1])
        top = (coord[3][0]-coord[1][0],coord[3][1]-coord[1][1])
        left = (coord[1][0]-coord[0][0],coord[1][1]-coord[0][1])
        right = (coord[3][0]-coord[2][0],coord[3][1]-coord[2][1])
        # panel section horizontal
        for sec in (1/3,2/3):
            s3 += 'M%s,%s l%s,%s ' % (
                round(x+coord[0][0]+left[0]*sec,3),
                round(y-coord[0][1]-left[1]*sec,3),
                round((right[0]-left[0])*sec+bottom[0],3),
                round(-(right[1]-left[1])*sec-bottom[1],3)
            )
        # panel section vertical
        for sec in (1/4,1/2,3/4):
            s3 += 'M%s,%s l%s,%s ' % (
                round(x+coord[0][0]+bottom[0]*sec,3),
                round(y-coord[0][1]-bottom[1]*sec,3),
                round((top[0]-bottom[0])*sec+left[0],3),
                round(-(top[1]-bottom[1])*sec-left[1],3)
            )
    # central wire
    s2 += 'M%s,%s l%s,%s' % (
        round(x+coord_m[0],3),round(y-coord_m[1],3),
        round(cc_m[0]-coord_m[0],3),round(coord_m[1]-cc_m[1],3)
    )
    s = '''    <path
       fill="none" stroke="#C0C0C0" stroke-width="0.5"
       d="%s" />
    <path
       fill="rgba(192,192,192,0.50)" stroke="#808080" stroke-width="1"
       d="%s" />
    <path
       fill="none" stroke="#808080" stroke-width="1"
       d="%s" />
''' % (s3,s1,s2)
    s += '''    <path
       fill="none" stroke="%s"
       d="M%s,%s h%s l%s,%s v%s l%s,%s l%s,%s l%s,%s z m%s,0 v%s l%s,%s m%s,%s l%s,%s" />
''' % (
        color,round(x,3),round(y,3),round(b,4),round(p,4),round(-yu,4),
        round(yu-ym,4),round(-0.5*b,4),round(ym-yo,4),round(-p,4),
        round(yo-h2,4),round(-0.5*b,4),round(h2-h1,4),round(b,4),
        round(-h1,4),round(-0.5*b,4),round(h1-h2,4),round(0.5*b,4),
        round(h2-h1,4),round(p,4),round(h1-ym,4)
    )
    # text and battery symbol
    if battery:
        # PV with battery
        s += '    <text x="%s" y="%s" fill="%s" text-anchor="middle" font-family="sans-serif" font-size="28" font-weight="500">PV</text>\n' % (round(x+0.5*b,3),round(y-h1-5,3),color)
        s += '    <text x="%s" y="%s" fill="%s" text-anchor="middle" font-family="sans-serif" font-size="18" font-weight="500">Battery</text>\n' % (round(x+0.5*b,3),round(y-h1+10,3),color)
        bat_b = round(b*40/74,1)
        bat_h = round(bat_b*21/40,1)
        s += '''    <path
       fill="rgba(224,224,224,0.50)" stroke="%s"
       d="M%s,%s h%s v%s h%s z" />
''' % (color,round(x+0.5*(b-bat_b),3),round(y-7,3),bat_b,-bat_h,-bat_b)
        s += '''    <path
       fill="none" stroke="%s"
       d="M%s,%s v-3 h1.5 v3 m%s,0 v-3 h1.5 v3 m0,6 h-6 m%s,0 h-6 m3,-3 v6" />
''' % (color,round(x+0.5*(b-bat_b)+3,3),round(y-7-bat_h,3),bat_b-9,-bat_b+18)
    else:
        # PV without battery
        s += '    <text x="%s" y="%s" fill="%s" text-anchor="middle" font-family="sans-serif" font-size="40" font-weight="700">PV</text>\n' % (round(x+0.5*b,3),round(y-17,3),color)
    # height at arrow location: (ym-h1 + h1)/2
    s += epfeil(x+b+p/2,y-yu/2-ym*0.5*0.12,factor=ym*0.5*0.9,color=color,pers=math.atan2(ym-h1,p)+0.1)
    return s

def pv(b,h,unit,battery,color,background_color,text):
    """ Feuerwehrzeichen PV-Anlage
    
        Args:
            b (int, float): external width
            h (int, float): external height
            battery (bool): with or without battery
            color (str): line and text color
            background_color (str): background color or "none"
    """
    ratio = b/h
    b_coord = round(HEIGHT*ratio,3)
    h_coord = HEIGHT
    if text:
        # lines of text below the icon
        if isinstance(text,list):
            lines_count = len(text)
        else:
            lines_count = 1
        h_text = h_coord-20-10*lines_count
        h_house = h_text-(10 if lines_count==1 else 5)
    else:
        # no text below the icon
        h_house = h_coord-22
    s = WW_XML
    s += WW_SVG1 % (b,unit,h,unit,b_coord,h_coord)
    if battery:
        s += '  <desc lang="de">Feuerwehrzeichen PV-Anlage mit Batterie</desc>\n'
    else:
        s += '  <desc lang="de">Feuerwehrzeichen PV-Anlage</desc>\n'
    if background_color!='none':
        s += '  <rect x="0" y="0" width="%s" height="%s" fill="%s" stroke="none" />\n' % (round(b_coord,3),round(h_coord,3),background_color)
    s += WW_SVG_G
    s += sonne(b_coord-BORDER1-BORDER2,BORDER1,33,color)
    # border
    s += rand(BORDER1,BORDER1,b_coord-2*BORDER1,h_coord-2*BORDER1,BORDER2,SIGNAL_RED)
    if text:
        border = BORDER1+BORDER2-0.1
        s += '    <path\n       fill="%s" stroke="none"\n       d="M%s,%s h%s v%s h%s z" />\n' % (SIGNAL_RED,border,h_text,b_coord-2*border,BORDER2,-b_coord+2*border)
        s += '    <text x="%s" y="%s" text-anchor="middle" font-family="sans-serif" font-size="12">%s</text>\n' % (b_coord/2,h_coord-BORDER1-BORDER2-3,text[1] if isinstance(text,list) else text)
        if lines_count>1:
            s += '    <text x="%s" y="%s" text-anchor="middle" font-family="sans-serif" font-size="12">%s</text>\n' % (b_coord/2,h_coord-BORDER1-BORDER2-14,text[0])
    # house with PV panels
    s += haus(0.5*(b_coord-116),h_house,battery,color)
    s += WW_SVG2
    return s

#print(pv(WIDTH,HEIGHT,False,'none'))
#print(pv(150,200,False,'none'))
#print(pv(146,188,True,'#F0F0B0'))

b,h=WIDTH,HEIGHT
b,h=150,200
b,h=146,188
unit = ''

pv_list = (
    ('firesafety-pv.svg',pv,False,146,188,'mm',None),
    ('firesafety-pv-battery.svg',pv,True,146,188,'mm',None),
    ('firesafety-pv-emergency-power.svg',pv,True,146,208,'mm','mit Notstrom'),
    ('firesafety-pv-black-start.svg',pv,True,146,208,'mm',['Ersatzstrom und','Schwarzstartfähigkeit']),
)

if True:

    usage = "Usage: %prog [options]"
    epilog = 'UNIT may be "px", "em", "mm", "cm" etc. or no unit.'

    # Create a command line parser:
    parser = optparse.OptionParser(usage=usage, epilog=epilog)
    
    parser.add_option('--size',dest='size',
                      default='auto',
                      metavar='SIZE',
                      help='dimension "WIDTHxHEIGHT[UNIT]" or "A4" to "A7"')
    parser.add_option('--color',dest='color',
                      default='#000000',
                      metavar='COLOR',
                      help='line and text color ("currentColor" for embedding)')
    parser.add_option('--background-color',dest='bkcolor',
                      default=SIGNAL_WHITE,
                      metavar='COLOR',
                      help='background color or "none" if transparent')

    (options, args) = parser.parse_args()
    
    if options.size:
        if options.size.lower()=='auto':
            b = None
            h = None
            unit = None
        elif options.size.upper()=='A7':
            b = 74
            h = 105
            unit = 'mm'
        elif options.size.upper()=='A6':
            b = 105
            h = 148
            unit = 'mm'
        elif options.size.upper()=='A5':
            b = 148
            h = 210
            unit = 'mm'
        elif options.size.upper()=='A4':
            b = 210
            h = 297
            unit = 'mm'
        else:
            x = options.size.split('x')
            x1 = []
            x2 = []
            for c in x[1]:
                if c.isdigit() or c=='.':
                    x1.append(c)
                elif c!=' ':
                    x2.append(c)
            b = int(x[0].strip())
            h = int(''.join(x1))
            unit = ''.join(x2)
    
    if b and h:
        print('icon size: %sx%s %s' % (b,h,unit))
    else:
        print('icon size: auto')
    print('line and text color: %s' % options.color)
    print('background color: %s' % options.bkcolor)

for i in pv_list:
    text = i[6]
    if b and h:
        print('creating %s' % i[0])
        s = i[1](b,h,unit,i[2],options.color,options.bkcolor,text)
    else:
        print('creating %s (%sx%s%s)' % (i[0],i[3],i[4],i[5]))
        s = i[1](i[3],i[4],i[5],i[2],options.color,options.bkcolor,text)
    with open(i[0],'wt') as f:
        f.write(s)
