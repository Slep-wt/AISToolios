import xml.etree.ElementTree as et
import numpy as np
import glob,os,sys

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

if not os.path.exists(KMLDIR):
    os.makedirs(KMLDIR)

for file in glob.glob(KMLDIR+'\\*_PARKING.kml'):
    print(file)
    filename = file
    tree = et.parse(filename)
    bays = {}

    for pm in tree.iterfind('.//{0}Placemark'.format(ns)):
        name = pm.find('{0}name'.format(ns)).text

        for ls in pm.iterfind('{0}Point/{0}coordinates'.format(ns)):
            rcoords = [ToISO(float(i)) for i  in ls.text.strip().replace('\n','')[:-2].split(',')[::-1]]
            coords = rcoords[0]+rcoords[1]
            bays[name] = coords

    sorted_bays = dict(sorted(bays.items()))
    filename = filename.replace('kml','xml');
    if not os.path.exists('Coords'):
        os.makedirs('Coords')
    with open('Coords\\' + filename.replace(KMLDIR + '\\', ''), 'w') as f:
        f.write('<!--' + filename.replace('_PARKING.xml','') + ' Parking Coordinates-->\n')
        for key, value in sorted_bays.items():
            f.write('<Point Name="'+key+'">'+value+'</Point>\n')
    



