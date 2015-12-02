# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# CADManagementScript.py
# Usage: CADManagementScript <NumeroDeControl> <ArchivoComprimidoZipConCADs> <NombreVersion> 
# Description: 
# Modelo de geoprocesamiento que se utiliza para hacer la carga de los archivos CADs a la aplicación Web.
# ---------------------------------------------------------------------------

#arcpy module import
import arcpy, os, sys

#import main .py files
import LoadCadToWeb
import Tools
#set the necessary product code
import arceditor


###toolboxes*******
##try:
##    arcpy.ImportToolbox("C:\\ManejoCAD\\CADManagement.tbx")
##    arcpy.AddMessage("toolbox imported")
##except Exception:
##    e = sys.exc_info()[1]
##    print(e.args[0])
##    print("tratando de importar toolBox")
##    arcpy.AddError(e.args[0])
##
###end toolboxes*****
try:
    #Workspace******
    try:
        print(sys.path[0])
        arcpy.AddMessage(sys.path[0])
        arcpy.env.scratchWorkspace = sys.path[0]
        ##arcpy.env.scratchWorkspace = r"c:\ManejoCAD\scratch"
        ##arcpy.env.scratchWorkspace = arcpy.env.scratchFolder
        arcpy.AddMessage("****scratchworkspace Set*****")
        arcpy.AddMessage(arcpy.env.scratchWorkspace)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        print("seteando ScratchWorkspace")
        arcpy.AddMessage(e.args[0])
              
    #Alias: CADManagement


    #Parameters and variables section*************
    #script argument
    ##con = input("entra numero de control: ")
    ##
    ##NumeroDeControl = con
    ##ArchivoComprimidoZipConCADs = "c:\\ManejoCAD\\2015-01485.zip"
    ##NombreVersion = "giseditor.edicionweb"

    try:
        NumeroDeControl = arcpy.GetParameterAsText(0)
        ArchivoComprimidoZipConCADs = arcpy.GetParameterAsText(1)
        NombreVersion = arcpy.GetParameterAsText(2)
        arcpy.AddMessage("variables found")
        arcpy.AddMessage(NumeroDeControl)
        arcpy.AddMessage(ArchivoComprimidoZipConCADs)
        arcpy.AddMessage(NombreVersion)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        print("Buscando Variables")
        arcpy.AddMessage(e.args[0])
    #***************

    #local variables
    try:
        instancia = "gmtserver3"
        v_scratchFolder = arcpy.env.scratchFolder
        print("folderScratch: " + v_scratchFolder)
        conexionGDBsde = v_scratchFolder
        cadDescomprimido = os.path.join(arcpy.env.scratchWorkspace,"cadDescomprimido")
        print(cadDescomprimido)
        arcpy.AddMessage("local variables declared")
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        print("declarando variables locales")
        arcpy.AddMessage(e.args[0])
    #***************
    #End parameters and variable section**********

    #Process structure: arcpy.NameOfThePRocess_AliasOfTheToolbox

    #process: Create the Db connection
    #call the CreateDatabaseConnection located in the toolbox
    try:
        ##arcpy.CreateDatabaseConnection_CADManagement(NombreVersion, instancia, v_scratchFolder)
        OutputDB = Tools.CreateDatabaseConnection(NombreVersion, instancia, v_scratchFolder)
        arcpy.AddMessage("database connection declared")
        arcpy.AddMessage(OutputDB)
        print(OutputDB)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        print("creando coneccion base datos")
        arcpy.AddMessage(e.args[0])

    #process: uncompress Zip
    #call the script to uncompress the zip file
    try:
        ##arcpy.UnCompressZipCad_CADManagement(ArchivoComprimidoZipConCADs, cadDescomprimido)
        Tools.UnCompressZipCad(ArchivoComprimidoZipConCADs, cadDescomprimido)
        arcpy.AddMessage("file descomprimido")
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        print("llamando funcion descomprimir archivo")
        arcpy.AddMessage(e.args[0])
        
    #print cadDescomprimido

    ##for dirName, subdirList, fileList in os.walk(cadDescomprimido):
    ##    print("dound directoryL %s" % dirName)
    ##    arcpy.AddMessage("dound directoryL %s" % dirName)
    ##    for fname in fileList:
    ##        print("\t%s" % fname)
    ##        arcpy.AddMessage("\t%s" % fname)
    #call the process to load the cad to the web
    arcpy.AddMessage("entrando a loadear loc CAD")
    print("entrando a loadear loc CAD")
    ##arcpy.LoadCadToWeb_CADManagement(NumeroDeControl, cadDescomprimido, v_scratchFolder)
    LoadCadToWeb.LoadCadToWeb(NumeroDeControl, cadDescomprimido, v_scratchFolder)
    arcpy.AddMessage("End of code") 
except Exception:
    ex = sys.exc_info()[1]
    print(ex.args[0])
    arcpy.AddMessage(ex.args[0])
