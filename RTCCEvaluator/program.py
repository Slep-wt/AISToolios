import xml.etree.ElementTree as et
import numpy as np
import glob,os
import re

ns = '{http://www.opengis.net/kml/2.2}'

KMLDIR = 'GoogleEarth'
XMLDIR = 'Coords'
def ToISO(dd):
    assembly = ''
    if (np.sign(dd) == 1):
        assembly += '+' + str(round(dd,7))
    else:
        assembly += str(round(dd,7))
    return assembly

def ReadLines(ls):
    linepoints = []
    vec3 = []
    for x in ls.text.split(' '):
        vec3.append(x.strip().split(','))

    for x in vec3:
        if len(x) == 3:
            oarr = [ToISO(float(x[1])), ToISO(float(x[0]))]
            linepoints.append(oarr)
    return linepoints


def ReadPoints(ls):
    points = []
    vec3 = []
    for x in ls.text.split(' '):
        vec3.append(x.strip().split(','))

    for x in vec3:
        if len(x) == 3:
            oarr = [ToISO(float(x[1])), ToISO(float(x[0]))]
            points.append(oarr)
    return points

def main():
    if not os.path.exists(KMLDIR):
        os.makedirs(KMLDIR)

    for file in glob.glob(KMLDIR+'\\*_RTCC.kml'):
        print(file)
        filename = file
        tree = et.parse(filename)
        lines = {}
        points = {}
        for pm in tree.iterfind('.//{0}Placemark'.format(ns)):
            name = pm.find('{0}name'.format(ns)).text
            linepoints = []
            for ls in pm.iterfind('.//{0}LineString//{0}coordinates'.format(ns)):
                lines[name] = ReadLines(ls)
            for ls in pm.iterfind('.//{0}LinearRing//{0}coordinates'.format(ns)):
                lines[name] = ReadLines(ls)
            for ls in pm.iterfind('.//{0}Point//{0}coordinates'.format(ns)):
                points[name] = ReadPoints(ls)

        rtccLines = dict(sorted(lines.items()))
        rtccPoints = dict(sorted(points.items()))
        filename = filename.replace('kml','xml')

        location = re.compile(r"\\([A-Z]*)\_RTCC")
        result = location.search(filename)
        if (result == None):
            print("Invalid file name: {filename}. Please fix and re-run.")
            return
        ad = result.group(1)
        
        if not os.path.exists('Coords'):
            os.makedirs('Coords')
        with open(f'Coords\\' + filename.replace(KMLDIR + '\\', ''), 'w') as fl:

            fl.write(f'<?xml version="1.0" encoding="utf-8"?>\n<Maps>\n<Map Type="System2" Name="{ad} RTCC" Priority="2" Center="0+0">')
            fl.write(f'<!-- {ad} RTCC Lines-->\n')
            for key, values in rtccLines.items():
                fl.write(f'<!-- {key} -->\n')
                fl.write('<Line Pattern="Dotted" Width="1.5">\n')
                fl.write('<Point>')
                listlen = len(values)-1
                for index, x in enumerate(values):
                    if (index == listlen):
                        fl.write(str(x[0])+str(x[1]))
                    else:
                        fl.write(str(x[0])+str(x[1])+'/')
                fl.write('</Point>\n')
                fl.write('</Line>\n')
            for key, value in rtccPoints.items():
                fl.write(f'<!-- MVA{key} -->\n')
                fl.write('<Label HasLeader="false">\n')
                fl.write(f'<Point Name="{key}">{value[0][0]}{value[0][1]}</Point>\n')
                fl.write('</Label>\n')
            fl.write('</Map>\n')
            fl.write('</Maps>\n')
    
if __name__ == '__main__':
    main()


