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

WW_XML = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
WW_SVG1 = '<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="%s" height="%s" viewBox="-46 -46 92 92">'
WW_SVG2 = '</svg>\n'

SUN_COLOR   = "#f6bc68"
MOON_COLOR  = "#da4935"
CLOUD_COLOR = "#828487"
RAIN_COLOR  = "#66a1ba"
# SAND_COLOR #a95c33 #a96132 #a47137
SAND_COLOR = '#a96132'

SPRING_COLOR = '#90be66'
SUMMER_COLOR = '#f6bc68'
AUTUMN_COLOR = '#e37e54'
WINTER_COLOR = '#66a1ba'

SEASONS_COLORS = {'spring':SPRING_COLOR,'summer':SUMMER_COLOR,'autumn':AUTUMN_COLOR,'winter':WINTER_COLOR}


def sonne(x=0, y=0, color=SUN_COLOR, fill="none"):
    """ sun icon """
    s = '<g stroke="%s" stroke-width="%s">' % (color,4)
    s += '<circle cx="%s" cy="%s" r="18" fill="%s" />' % (x,y,fill)
    s += '<path fill="none" d="'
    for i in range(8):
        w = math.pi*i/4
        ri = 24
        ro = 38
        s += 'M %s,%s L %s,%s ' % (round(x+math.cos(w)*ri,14),round(y+math.sin(w)*ri,14),round(x+math.cos(w)*ro,14),round(y+math.sin(w)*ro,14))
    s += '" />'
    s += '</g>'
    return s

def schneeflocke(x, y, r, innen=True, color=RAIN_COLOR):
    """ snowflake """
    y -= r
    s = '<path stroke="%s" stroke-width="%s" stroke-linecap="round" fill="none" d="M %s,%s ' % (color,4,x,y) # stroke-width was r*0.15
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

def flower(x, y, r, color, fill='none', count=6, petal='6,0.4308', debug=False):
    s = petal.split(',')
    # count of petals
    count = int(s[0])
    # shape of the petal
    petal = s[1]
    s = ['<g stroke="%s" stroke-width="%s">' % (color,4)]
    s.append('<circle cx="%s" cy="%s" r="10" fill="%s" />' % (x,y,fill))
    alpha = 2.0*math.pi/count
    alpha2 = math.pi/count
    ri = 10
    if petal=='circle':
        # Kreis
        ro = r/(1/math.cos(alpha2)+math.tan(alpha2))
        a = b = rr = ro*math.tan(alpha2)
        print('ro=%.2f rr=%.2f' % (ro,rr))
    elif petal=='Steiner':
        # Steiner's Ellipse
        h = r
        cc = h/2*math.tan(alpha2)
        ro = math.sqrt(cc*cc+(h/2)*(h/2))
        b = h/3
        a = math.tan(alpha2)*h/math.sqrt(3)
        #rd = h/math.cos(alpha2)
        print('h=%.2f cc=%.2f ro=%.2f a=%.2f b=%.2f' % (h,cc,ro,a,b))
    else:
        # General ellipse (b<0.5 required)
        h = r
        b = float(petal)*h # chosen value
        c2 = h*math.tan(alpha2)
        a = c2*math.sqrt(1-2*b/h)
        y_ro = h-b*h/(h-b)
        x_ro = c2*(h-2*b)/(h-b)
        ro = math.sqrt(y_ro*y_ro+x_ro*x_ro)
        print('h=%.2f c2=%.2f ro=%.2f a=%.2f b=%.2f' % (h,c2,ro,a,b))
    if debug:
        s.append('<circle cx="0" cy="0" r="%s" fill="none" stroke="red" stroke-width="1" />' % ro)
        s.append('<circle cx="0" cy="0" r="%s" fill="none" stroke="red" stroke-width="1" />' % r)
        #s.append('<circle cx="0" cy="0" r="%s" fill="none" stroke="red" />' % rd)
    s.append('<path fill="none" d="')
    for i in range(count):
        w = alpha*i
        s.append('M%s,%s' % (round(x+math.cos(w)*ri,14),round(y+math.sin(w)*ri,14)))
        if ro>ri:
            s.append('L%s,%s' % (round(x+math.cos(w)*ro,14),round(y+math.sin(w)*ro,14)))
        w = alpha*(i+1)
        s.append('A%s,%s %s 1 1 %s,%s' % (b,a,360/count*(i+0.5),round(x+math.cos(w)*ro,14),round(y+math.sin(w)*ro,14)))
    s.append('" />')
    s.append('</g>\n')
    return ''.join(s)

def seasons_symbol(season, filled, background, petal='6,0.4308', debug=False):
    """ create symbols for the four seasons
    """
    # symbol color depending on season
    color = SEASONS_COLORS[season]
    # description and copyright
    s = [
        '  <desc>%s season</desc>\n' % season,
        '  <!-- Copyright (C) 2026 Johanna Karen Rödenbeck -->\n'
    ]
    # background color
    if background.lower()=='round':
        # white symbol on colored round background
        fgcolor = '#ffffff'
        s.append('  <circle cx="0" cy="0" r="46" stroke="none" fill="%s" />\n' % color)
    elif background.lower()=='square':
        # white symbol on colored square background
        fgcolor = '#ffffff'
        s.append('  <rect x="-46" y="-46" width="92" height="92" stroke="none" fill="%s" />\n' % color)
    else:
        # colored symbol on translucent background
        fgcolor = color
    # the symbol iteself depending on season
    if season=='spring':
        # flower as a symbol for spring
        s.append(flower(0,0,38,color=fgcolor,fill=fgcolor if filled else 'none',petal=petal,debug=debug))
    if season=='summer':
        # sun as a symbol for summer
        s.append('  ')
        s.append(sonne(0,0,color=fgcolor,fill=fgcolor if filled else 'none'))
        s.append('\n')
    if season=='autumn':
        # a falling leave as a symbol for autumn
        pass
    if season=='winter':
        # a snowflake as symbol for winter
        s.append('  ')
        s.append(schneeflocke(0,0,38,color=fgcolor))
        s.append('\n')
    return ''.join(s)


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
    parser.add_option("--background", action="store",
                      default='translucent',
                      help="background (translucent, square, round)")
    parser.add_option("--petal", action="store",
                      default="6,0.4",
                      help="petal count and shape, default 6,0.4308")
    parser.add_option("--width", action="store",
                      default=100,
                      help="width and height of the image, default 100")
    parser.add_option("--debug", action="store_true",
                      default=False,
                      help="debugging output")

    (options, args) = parser.parse_args()


    if options.writesvg:

        filled = options.filled
        for val in ['spring','summer','autumn','winter']:
            with open(val+'.svg','w') as file:
                file.write(WW_XML)
                file.write(WW_SVG1 % (options.width,options.width))
                file.write(seasons_symbol(val,filled,options.background,petal=options.petal,debug=options.debug))
                file.write(WW_SVG2)
    
    elif options.writepy:
    
        pass
    
    else:
    
        parser.print_help()
