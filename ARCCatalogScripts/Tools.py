# -*- coding: utf-8 -*-

import arcpy, sys, zipfile, os, traceback, arceditor
from os.path import isdir, join, normpath, split

##*****Call fucntion that will execute the uncompressed function on the selected file
def UnCompressZipCad(inFile, outFile):
    print("******enFuncionUnCompressed")
    print(inFile)
    print(outFile)
    try:
        zip = zipfile.ZipFile(inFile, 'r')
        unzip(outFile, zip)
        zip.close()
    except Exception:
        # Return any Python specific errors and any error returned by the geoprocessor
        #
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        arcpy.AddError(pymsg)

        msgs = "GP ERRORS:\n" + arcpy.GetMessages(2) + "\n"
        arcpy.AddMessage(msgs)
        print(msgs)
        print(sys.exc_info()[1])
    return

##**********function to unzip the selected compressed folder
def unzip(path, zip):
    print ("unzip")
    arcpy.AddMessage("unzip")
    ##If the output location does not exist crate it
    if not isdir(path):
        os.makedirs(path)

    for each in zip.namelist():
        arcpy.AddMessage("Extracting " + os.path.basename(each) + " ...")
        # Check to see if the item was written to the zip file with an
        # archive name that includes a parent directory. If it does, create
        # the parent folder in the output workspace and then write the file,
        # otherwise, just write the file to the workspace.
        #
        if not each.endswith('/'):
            root, name = split(each)
            directory = normpath(join(path,root))
            if not isdir(directory):
                os.makedirs(directory)
            file(join(directory, name), 'wb').write(zip.read(each))
    return

##*******
# Create DAtabaseConnection, if it exist id recreates it if no
# it simply create it
##*******
def CreateDatabaseConnection(NombreVersion, Instance, scratchFolder):
    # Output Overwirte
    arcpy.env.overwriteOutput = True

    #delete connection if exist
    arcpy.AddMessage("********Inside Tools.CreateDatabaseConnection")
    if os.path.exists(arcpy.env.scratchFolder + "\Conexion_GDB.sde"):
        os.remove(arcpy.env.scratchFolder + "\Conexion_GDB.sde")

    outputfile = arcpy.CreateDatabaseConnection_management(arcpy.env.scratchFolder, "Conexion_GDB.sde", "SQL_SERVER", Instance, "DATABASE_AUTH", "giseditor", "giseditor", "SAVE_USERNAME", "CDPR", "", "TRANSACTIONAL", NombreVersion, "")
    arcpy.AddMessage(arcpy.env.scratchFolder)
    arcpy.AddMessage(outputfile)
    print(arcpy.env.scratchFolder)
    print(outputfile)
    return outputfile

##*******
# CAD data conversion to geodatabase format data
##*******
def CadToGeodatabase(CAD, ScratchGDB,state):
    spatial_reference = "NAD_1983_StatePlane_Puerto_Rico_Virgin_Islands_FIPS_5200"
    print("insideCadToGeo")
    try:
        #process: convert_FC-DefProj
        arcpy.CADToGeodatabase_conversion(CAD, ScratchGDB, "CAD", "1000", "")
        arcpy.AddMessage("converison success")
        print("conversion Success")
    except Exception:
        print((sys.exc_info()[1]).args[0])
    return

##************
# this is use for some kind of annotation
##************
def annotationFeature():
    # Set environment settings - user specified
    # User input geodatabase for annotation location - eg. C:/data/roads.gdb
    arcpy.env.workspace = "C:\Temp\CRIM\scratch.gdb\CAD\Annotation"

    # Create list of annotation feature classes within the geodatabase
    fcList = arcpy.ListFeatureClasses("", "ANNOTATION")

    # Set variables
    # User input output feature class name - eg. appendedroadsAnno
    outFeatureClass = arcpy.env.workspace + os.sep + "Database Connections\giseditor@CDPR@gmtserver3.sde\CDPR.GISEDITOR.Anotaciones_CADs"
    refScale = 1200
    createClasses = "CREATE_CLASSES"
    symbolReq = "NO_SYMBOL_REQUIRED"
    autoCreate = "AUTO_CREATE"
    autoUpdate = "AUTO_UPDATE"

    # Process: Append the annotation feature classes
    print("Appending annotation feature classes...")
    arcpy.AppendAnnotation_management(fcList, outFeatureClass, refScale, createClasses, symbolReq, autoCreate, autoUpdate)

    print("Annotation feature classes in " + arcpy.env.workspace + " have been appended into " + outFeatureClass)
    return

