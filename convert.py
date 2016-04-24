#!/usr/local/bin/python

import sys, getopt, os, xml.etree.ElementTree as ET

def main():
    global inputFile
    global outputDir
    global targetModule
    global overwrite

    # Get the options passed into the commandline    
    getOptions(sys.argv[1:])
    
    if(inputFile == ''):
        print("Input library has not been defined")
        sys.exit()
        
    # Prepare the output directory
    prepareDirectory(outputDir)

    # Validate Input file
    if not (os.path.isfile(inputFile) and os.access(inputFile, os.R_OK)):
        print "Input library is either missing or is not readable"
        sys.exit();

    # Read the XML input
    tree = ET.parse(inputFile)
    root = tree.getroot()

    # Run through the footprints
    for child in root[0][3][1]:
        parseChildParameter(child)    
    return;

# Write to the output file.
def writeToFootprintFile(packageFile, dataLine):
    f = open(packageFile, "a+")
    f.write(dataLine)
    return

# Parse the child parameters to find the packages
def parseChildParameter(child):
    if child.tag == "package":
        processPackage(child);
    return

def processPackage(package):
    global overwrite, targetModule
    
    packageName = package.attrib.get('name')
    packageFile = outputDir + "/" + packageName + ".kicad_mod"

    if (targetModule == '' or targetModule == packageName):

        # If the file exists and overwrite is specified then we delete the file    
        if (os.path.isfile(packageFile) and overwrite):
            os.remove(packageFile)

        elif (os.path.isfile(packageFile) and not overwrite):
            print("Footprint for " + packageName + " exists, skipping...")
            return
        
        writeToFootprintFile(packageFile, "(module REF** (layer F.Cu) (tedit 55E4F891)\n")

        for child in package:
           if child.tag == "text":
               processText(packageName, packageFile, child);

        for child in package:
            if child.tag == "wire":
                processWire(packageName, packageFile, child);
            if child.tag == "pad":
                processPad(packageName,  packageFile,child);
           # if child.tag == "smd":
           #     print(child.tag, child.attrib)
           # if child.tag == "rectangle":
           #     print(child.tag, child.attrib)
           # if child.tag == "circle":
           #     print(child.tag, child.attrib)

        # writeToFootprintFile(packageName, "  (model to/to18.wrl\n")
        # writeToFootprintFile(packageName, "    (at (xyz 0 0 0))\n")
        # writeToFootprintFile(packageName, "    (scale (xyz 1 1 1))\n")
        # writeToFootprintFile(packageName, "    (rotate (xyz 0 0 0))\n")
        # writeToFootprintFile(packageName, "  )\n")
        # writeToFootprintFile(packageName, ")\n")
    return

def processText(packageName, packageFile, text):

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
        

    writeToFootprintFile(packageFile, "  (fp_text " + textValue + " (at " + x + " " + y + "" + rotation + ") (layer " + layer + ") " + hide +"\n")
    writeToFootprintFile(packageFile, "   (effects (font (size 0.8 0.8) (thickness 0.15)))\n")
    writeToFootprintFile(packageFile, "  )\n")
    return

def processWire(packageName, packageFile, wire):
    width = wire.attrib.get('width');
    layer = wire.attrib.get('layer');
    x1 = wire.attrib.get('x1');
    y1 = wire.attrib.get('y1');
    x2 = wire.attrib.get('x2');
    y2 = wire.attrib.get('y2');
    curve = wire.attrib.get('curve');
    # layer = getMappedLayer(wire.attrib.get('layer'))
    
    writeToFootprintFile(packageFile, "  (fp_line (start "+x1+" "+y1+") (end "+x2+" "+y2+") (layer F.SilkS) (width " + width + "))\n")
    return;

# Create pads for 
def processPad(packageName, packageFile, pad):
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
    writeToFootprintFile(packageFile, "  (pad " + name + " thru_hole circle (at " + x + " " + y + ") (size " + str(xSize) + " " + str(ySize) +") (drill " + drill + ") (layers *.Cu *.Mask F.SilkS))\n")
    return;

# Get the commandline options
def getOptions(argv):
    global inputFile, outputDir, targetModule, overwrite

    # Get the options from the commandline
    try:
      opts, args = getopt.getopt(argv,"hi:o:t:x:",["ifile=","oDir=","targetMod=","overwrite="])
    except getopt.GetoptError:
      print 'convert.py -i <inputfile> -o <outputDirectory> [ -t <target-module-name>, -x true ]'
      sys.exit(2)

    for opt, arg in opts:
      if opt == '-h':
         print 'convert.py -i <inputFile> -o <outputDirectory> [ -t <target-module-name>, -x true ]'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputFile = arg
      elif opt in ("-o", "--oDir"):
         outputDir = arg
      elif opt in ("-t", "--targetMod"):
         targetModule = arg
      elif opt in ("-x", "--overwrite"):
         overwrite = True
    return

def prepareDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)    
    return


# Create global variables
inputFile = ''
outputDir = './Output.pretty'
targetModule = ''
overwrite = False

# Execute the script
main();