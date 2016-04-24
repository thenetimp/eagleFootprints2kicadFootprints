This is a script for ripping footprints out of libraries.  Currently it only works on through hole components, but I will work on making smd components work as well.

Basic Usage:
  convert.py -i <inputfile> -o <outputDirectory> [ -t <target-module-name>, -x true ]
    
  -i <inputfile>:  The eagle library that you'd like convert footprints for.
  
  -o <outputDirectory>: The name of the directory that you want to put the footprint files in.  
                   This should be a kicad footprint library
                   
  -t <target-module-name>:  If you only want a specific module from a library pass it with this argument.
  
  -x true: Overwrite the module's file exists overwrite it. 
  
  