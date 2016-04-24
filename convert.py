#!/usr/local/bin/python

import xml.etree.ElementTree as ET

def writeToFootprintFile(package, dataLine):
    f = open("TestPackage.pretty/" + package + ".kicad_mod", "a+")
    f.write(dataLine)
    return

def parseChildParameter(child):
    if child.tag == "package":
        processPackage(child);
    return

def processPackage(package):
    packageName = package.attrib.get('name')
    
    writeToFootprintFile(packageName, "(module REF** (layer F.Cu) (tedit 55E4F891)\n")
    
    for child in package:
       if child.tag == "text":
           processText(packageName, child);
    
    # writeToFootprintFile(packageName, "  (fp_text reference Q? (at 0 0) (layer F.SilkS)\n")
    # writeToFootprintFile(packageName, "   (effects (font (size 0.8 0.8) (thickness 0.15)))\n")
    # writeToFootprintFile(packageName, "  )\n")
    # writeToFootprintFile(packageName, "  (fp_text value " + packageName + " (at 0 0) (layer F.Fab) hide\n")
    # writeToFootprintFile(packageName, "   (effects (font (size 0.8 0.8) (thickness 0.15)))\n")
    # writeToFootprintFile(packageName, "  )\n")

    for child in package:
        if child.tag == "wire":
            processWire(packageName, child);
        if child.tag == "pad":
            processPad(packageName, child);
#        if child.tag == "smd":
#            print(child.tag, child.attrib)
#        if child.tag == "rectangle":
#            print(child.tag, child.attrib)
#        if child.tag == "circle":
#            print(child.tag, child.attrib)

    writeToFootprintFile(packageName, "  (model to/to18.wrl\n")
    writeToFootprintFile(packageName, "    (at (xyz 0 0 0))\n")
    writeToFootprintFile(packageName, "    (scale (xyz 1 1 1))\n")
    writeToFootprintFile(packageName, "    (rotate (xyz 0 0 0))\n")
    writeToFootprintFile(packageName, "  )\n")
    writeToFootprintFile(packageName, ")\n")
    return

def processText(packageName, text):

    x = text.attrib.get('x')
    y = text.attrib.get('y')
    rotation = text.attrib.get('rot');
    layer = text.attrib.get('layer');
    textValue = "";
    hide = "";

    if text.text == ">NAME":
        textValue = "value " + packageName
        layer = "F.Fab"
        hide="hide" 
         
    if text.text == ">VALUE":
        textValue = "reference REF**"
        layer = "F.SilkS" 
        hide = ""
        
    if rotation == "R90":
        rotation = " 90"
        print ("Rotating 90 degress...\n")
    else:
        rotation = ""    
        print ("No Rotation required...\n")
        

    writeToFootprintFile(packageName, "  (fp_text " + textValue + " (at " + x + " " + y + "" + rotation + ") (layer " + layer + ") " + hide +"\n")
    writeToFootprintFile(packageName, "   (effects (font (size 0.8 0.8) (thickness 0.15)))\n")
    writeToFootprintFile(packageName, "  )\n")
    return

def processWire(packageName, wire):
    width = wire.attrib.get('width');
    layer = wire.attrib.get('layer');
    x1 = wire.attrib.get('x1');
    y1 = wire.attrib.get('y1');
    x2 = wire.attrib.get('x2');
    y2 = wire.attrib.get('y2');
    curve = wire.attrib.get('curve');
    # layer = getMappedLayer(wire.attrib.get('layer'))
    
    writeToFootprintFile(packageName, "  (fp_line (start "+x1+" "+y1+") (end "+x2+" "+y2+") (layer F.SilkS) (width " + width + "))\n")
    return;

def processPad(packageName, pad):
    name = pad.attrib.get('name');
    shape = pad.attrib.get('shape');
    drill = pad.attrib.get('drill');
    baseSize = float(drill) * 1.75
    xSize = baseSize
    ySize = baseSize
    x = pad.attrib.get('x');
    y = pad.attrib.get('y');
    rotation = pad.attrib.get('rot');
    print("Write pad: " + name)
    writeToFootprintFile(packageName, "  (pad " + name + " thru_hole circle (at " + x + " " + y + ") (size " + str(xSize) + " " + str(ySize) +") (drill " + drill + ") (layers *.Cu *.Mask F.SilkS))\n")
    return;


tree = ET.parse('triac.lbr')
root = tree.getroot()

for child in root[0][3][1]:
    parseChildParameter(child)