# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# LoadCadToWeb.py
# Usage: LoadCadToWeb <Numero_de_Caso> <cadDescomprimido> <ConexionGDB> 
# Description: 
# Herramienta para convertir archivos de CAD a feature class.
# ---------------------------------------------------------------------------

#import arcpy module
import arcpy, os 

# Import modules

import sys
import traceback
import CalculaYCargaScript
import Tools
#toolboxes************
##arcpy.ImportToolbox("c:\ManejoCAD\CADManagement.tbx")
#Alias: CADManagement
#*********************
def LoadCadToWeb(Numero_de_Caso, cadDescomprimido, ConexionGDB):
    #Parameters/Variables***************
    #scriptarguments in the module for later
    ##Numero_de_Caso = arcpy.GetParameterAsText(0)
    ##
    ##cadDescomprimido = arcpy.GetParameterAsText(1)
    ##
    ##ConexionGDB = arcpy.GetParameterAsText(2)
    print("DENTRO DE LOAD CAD TO WEB")
    print(Numero_de_Caso)
    print(cadDescomprimido)
    print(ConexionGDB)
    
    arcpy.AddMessage(Numero_de_Caso)
    arcpy.AddMessage(cadDescomprimido)
    arcpy.AddMessage(ConexionGDB)
    
    ### Set local variables
    ##cadDescomprimido = "c:\\ManejoCAD\\cadDescomprimido"
##    ScratchGDB = "c:\\ManejoCAD\\scratch\\scratch.gdb"
##    CAD_StatePlane = "c:\\ManejoCAD\\scratch\\scratch.gdb\\CAD"
##    CAD_DefPrj = "C:\\ManejoCAD\\scratch\\scratch.gdb\\CAD"
    ScratchGDB = os.path.join(arcpy.env.scratchWorkspace,"scratch","scratch.gdb")
    CAD_StatePlane = os.path.join(arcpy.env.scratchWorkspace,"scratch", "scratch.gdb","CAD")
    CAD_DefPrj = os.path.join(arcpy.env.scratchWorkspace,"scratch","scratch.gdb","CAD")
    CADName =""

    #*************************

    #Main functionality*****************************

    ##for dirName, subdirList, fileList in os.walk(cadDescomprimido):
    ##    for fname in fileList:
    ##        print("\t%s" % fname)
    ##        CADName = os.path.splitext(fname)[0]
    ##        print("\t%s" % CADName)


    arcpy.env.workspace = cadDescomprimido

    datasets = arcpy.ListDatasets("*","All")

    for data in datasets:
        print data
        arcpy.AddMessage(data)
        CADName = os.path.splitext(data)[0]
        print CADName
        arcpy.AddMessage(CADName)
        ##arcpy.CheckCoordinateSystem_CADManagement(data)
        ##arcpy.CadToGeodatabase_CADManagement(data, ScratchGDB,CAD_StatePlane)
        ## Take a cad file an convert it to geodatabase features, creatin a file
        ## inside the scratch folder with this converted data.
        ##arcpy.DefineProjection_management
        ## if the data does not have a projection, it assign the projection
        #*****************************************************
        #************ Check coodinate system *****************
        # Set local variables
        prj = "" 
        ##indata = arcpy.GetParameterAsText(0)
        indata = data
        dsc = arcpy.Describe(indata) 
        sr = dsc.spatialReference 
        prj = sr.name.lower()
        try:   
           # check if indata is in StatePlane, has no PRJ, or one other than StatePlane
           if prj.find("nad_1983_stateplane_puerto_rico_virgin_islands_fips_5200") > -1:
               arcpy.AddMessage("Coordinate system is StatePlane")
               print ("Coordinate system is statePlane") 
               print(prj) 
               ##arcpy.CadToGeodatabase_CADManagement(data, ScratchGDB, CAD_StatePlane)
               Tools.CadToGeodatabase(data, ScratchGDB, CAD_StatePlane)
               ##arcpy.CalculaYCargaScript_CADManagement(CAD_DefPrj, Nombre_de_CAD, Numero_de_Caso, ConexionGDB)
               CalculaYCargaScript.CalculaYCargaScript(CAD_DefPrj, CADName, Numero_de_Caso, ConexionGDB)
           elif prj == "unknown": 
               arcpy.AddMessage("To continue, first define a coordinate system!")
               print ("To continue, first define a coordinate system!")
               print(prj)
               arcpy.DefineProjection_management(data, "PROJCS['NAD_1983_StatePlane_Puerto_Rico_Virgin_Islands_FIPS_5200',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',200000.0],PARAMETER['False_Northing',200000.0],PARAMETER['Central_Meridian',-66.43333333333334],PARAMETER['Standard_Parallel_1',18.03333333333333],PARAMETER['Standard_Parallel_2',18.43333333333333],PARAMETER['Latitude_Of_Origin',17.83333333333333],UNIT['Meter',1.0]]")
               ##arcpy.CadToGeodatabase_CADManagement(data, ScratchGDB, CAD_StatePlane)
               Tools.CadToGeodatabase(data,ScratchGDB, CAD_StatePlane)
               ##arcpy.CalculaYCargaScript_CADManagement(CAD_DefPrj, CADName, Numero_de_Caso, ConexionGDB)
               CalculaYCargaScript.CalculaYCargaScript(CAD_DefPrj, CADName, Numero_de_Caso, ConexionGDB)
           else:
               arcpy.AddMessage("Coordinate system is not StatePlane or Unknown")
               print ("Coordinate system is not StatePlane or Unknown")
        except Exception:
            ##AddPrintMessage(e[0], 2)
            ##print(e[0])
            print ((sys.exc_info()[1]).args[0])
    return
