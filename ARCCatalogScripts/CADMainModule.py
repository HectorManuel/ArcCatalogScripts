# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
# CADManagement.py
# Usage: CADManagement <NumeroDeControl> <ArchivoComprimidoZipConCADs> <NombreVersion> 
# Description: 
# Modelo de geoprocesamiento que se utiliza para hacer la carga de los archivos CADs a la aplicacion Web.
# Company: Gepgraphic Mapping Technologies
# Developer : Hector M. Asencio
# ---------------------------------------------------------------------------

#arcpy module import
import arcpy, os, sys, traceback, zipfile
from os.path import isdir, join, normpath, split

#set the necessary product code
import arceditor

##************************************************************
#
##          ** LoadCadToWeb Function **
#
##************************************************************

# ---------------------------------------------------------------------------
# LoadCadToWeb.py
# Usage: LoadCadToWeb <Numero_de_Caso> <cadDescomprimido> <ConexionGDB> 
# Description: 
# Herramienta para convertir archivos de CAD a feature class.
# ---------------------------------------------------------------------------

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
               CadToGeodatabase(data, ScratchGDB, CAD_StatePlane)
               ##arcpy.CalculaYCargaScript_CADManagement(CAD_DefPrj, Nombre_de_CAD, Numero_de_Caso, ConexionGDB)
               CalculaYCargaScript(CAD_DefPrj, CADName, Numero_de_Caso, ConexionGDB)
           elif prj == "unknown": 
               arcpy.AddMessage("To continue, first define a coordinate system!")
               print ("To continue, first define a coordinate system!")
               print(prj)
               arcpy.DefineProjection_management(data, "PROJCS['NAD_1983_StatePlane_Puerto_Rico_Virgin_Islands_FIPS_5200',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',200000.0],PARAMETER['False_Northing',200000.0],PARAMETER['Central_Meridian',-66.43333333333334],PARAMETER['Standard_Parallel_1',18.03333333333333],PARAMETER['Standard_Parallel_2',18.43333333333333],PARAMETER['Latitude_Of_Origin',17.83333333333333],UNIT['Meter',1.0]]")
               ##arcpy.CadToGeodatabase_CADManagement(data, ScratchGDB, CAD_StatePlane)
               CadToGeodatabase(data,ScratchGDB, CAD_StatePlane)
               ##arcpy.CalculaYCargaScript_CADManagement(CAD_DefPrj, CADName, Numero_de_Caso, ConexionGDB)
               CalculaYCargaScript(CAD_DefPrj, CADName, Numero_de_Caso, ConexionGDB)
           else:
               arcpy.AddMessage("Coordinate system is not StatePlane or Unknown")
               print ("Coordinate system is not StatePlane or Unknown")
        except Exception:
            ##AddPrintMessage(e[0], 2)
            ##print(e[0])
            print ((sys.exc_info()[1]).args[0])
    return


##************************************************************
#
##          ** CalculaYCarga Function **
#
##************************************************************

def CalculaYCargaScript(CAD, NombreCAD, NumeroDeControl, ConexionGDB):
                        
    #Script passed artguments
    ##CAD= arcpy.GetParameterAsText(0)
    ##NombreCAD = arcpy.GetParameterAsText(1)
    ##NumeroDeControl = arcpy.GetParameterAsText(2)
    ##ConexionGDB = arcpy.GetParameterAsText(3)
    print("DENTRO DE CALCULA Y CARGA")
    print(CAD)
    print(NombreCAD)
    print(NumeroDeControl)
    print(ConexionGDB)

    arcpy.AddMessage("DENTRO DE CALCULA Y CARGA")
    arcpy.AddMessage(CAD)
    arcpy.AddMessage(NombreCAD)
    arcpy.AddMessage(NumeroDeControl)
    arcpy.AddMessage(ConexionGDB)

    ##CAD = "C:\\ManejoCAD\\scratch\\scratch.gdb\\CAD"
    ##NombreCAD = "2015-01485"
    ##NumeroDeControl = "456"
    ##ConexionGDB = "c:\\ManejoCAD\\scratch\\Conexion_GDB.sde"

    base = "Conexion_GDB.sde"
    ##Omit the scratch, it came with the url I input
    
    tempUrl = os.path.join(ConexionGDB,base)
    ConexionGDB = tempUrl
    print (ConexionGDB)
    arcpy.AddMessage(ConexionGDB)
    #local variables
    puntosSeleccionados = CAD #\Point
    poligonosSelecionados = CAD #\Polyline
    lineasSeleccionadas = CAD #\Polygon

##    CDPRGidAdminPuntosCAD = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde\\CDPR.GISADMIN.Puntos_CAD"
##
##    CDPRGisAdminLineasCAD = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde\\CDPR.GISADMIN.Lineas_CAD"
##
##    CDPRGisAdminPoligonosCAD = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde\\CDPR.GISADMIN.Poligonos_CAD"
    CDPRGidAdminPuntosCAD = os.path.join(arcpy.env.scratchFolder,"Conexion_GDB.sde","CDPR.GISADMIN.Puntos_CAD")

    CDPRGisAdminLineasCAD = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde","CDPR.GISADMIN.Lineas_CAD")

    CDPRGisAdminPoligonosCAD = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde","CDPR.GISADMIN.Poligonos_CAD")
    #**********************************************
    #**********************************************

    #Puntos ---- Point
    try:
        # select points from CAD
        pointer = arcpy.SelectData_management(CAD,"Point")#\CAD \Point
        print(pointer)
        arcpy.AddMessage(pointer)
        #crear fields para el punto
        #agregar nombreCad Puntos
        arcpy.AddField_management(pointer, "Nombre_CAD","TEXT","","","50", "" ,"NULLABLE","NON_REQUIRED","")
        
        print("Nombre_Cad field Added")
        arcpy.AddMessage("Nombre_Cad field Added")
        #AgregarNumCaso
        arcpy.AddField_management(pointer, "Num_Control", "TEXT", "", "", "10", "","NULLABLE","NON_REQUIRED","")
        print("Num_Control field Added")
        arcpy.AddMessage("Num_Control field Added")
        ##Calcular y agregar el valor a los fields creados.
        #NombreCadPuntosCalculate
        
        arcpy.CalculateField_management(pointer, "Nombre_CAD", "'{0}'".format(NombreCAD), "PYTHON")
        print("'{0}'".format(NombreCAD))
        arcpy.AddMessage("'{0}'".format(NombreCAD))
        #NUmCasoPuntosCalculate
        
        arcpy.CalculateField_management(pointer, "Num_Control", "'{0}'".format(NumeroDeControl), "PYTHON")
        print("'{0}'".format(NumeroDeControl))
        arcpy.AddMessage("'{0}'".format(NumeroDeControl))

##        # Process: Clear Workspace Cache
##        arcpy.ClearWorkspaceCache_management(ConexionGDB)
##        arcpy.AddMessage("Workspace Cleared")

        #cargar Punto con su informacion
        TemporalEnvironment = arcpy.env.scratchWorkspace
        arcpy.AddMessage(TemporalEnvironment)
        
        ##arcpy.env.scratchWorkspace = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde"
        arcpy.env.scratchWorkspace = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde")
        arcpy.AddMessage(arcpy.env.scratchWorkspace)
        arcpy.Append_management(pointer, CDPRGidAdminPuntosCAD, "NO_TEST","Num_Control \"NÃƒÆ’Ã‚Âºm. de Control\" true false false 10 Text 0 0 ,First,#,\\Point,Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#,\\Point,Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#", "")
        arcpy.AddMessage("Append Complete")
        arcpy.env.scratchWorkspace = TemporalEnvironment
        arcpy.AddMessage(arcpy.env.scratchWorkspace)
        arcpy.AddMessage("point added")
        arcpy.TruncateTable_management(pointer)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddMessage(e.args[0])
        
        
    #**********************************************
    #**********************************************
        
    #lineas ---- Polyline
    try:
        # select points from CAD
        polyline = arcpy.SelectData_management(CAD,"Polyline")#\CAD \Polyline
        print(polyline)
        arcpy.AddMessage(polyline)
        #crear fields para el punto
        #agregar nombreCad Puntos
        arcpy.AddField_management(polyline, "Nombre_CAD","TEXT","","","50", "","NULLABLE","NON_REQUIRED","")
        print("Nombre_CAD field Added")
        arcpy.AddMessage("Nombre_CAD field Added")
        #AgregarNumCaso
        arcpy.AddField_management(polyline, "Num_Control", "TEXT", "", "", "10", "","NULLABLE","NON_REQUIRED","")
        print("Num_Control field Added")
        arcpy.AddMessage("Num_Control field Added")
        ##Calcular y agregar el valor a los fields creados.
        #NombreCadPuntosCalculate
        arcpy.CalculateField_management(polyline, "Nombre_CAD", "'{0}'".format(NombreCAD), "PYTHON")
        print("'{0}'".format(NombreCAD))
        #NUmCasoPuntosCalculate
        arcpy.CalculateField_management(polyline, "Num_Control", "'{0}'".format(NumeroDeControl), "PYTHON")
        print("'{0}'".format(NumeroDeControl))
        arcpy.AddMessage("'{0}'".format(NumeroDeControl))

##        # Process: Clear Workspace Cache
##        arcpy.ClearWorkspaceCache_management(ConexionGDB)
##        arcpy.AddMessage("Workspace clreared")
        #cargar Punto con su informacion
        TemporalEnvironment1 = arcpy.env.scratchWorkspace
        ##arcpy.env.scratchWorkspace = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde"
        arcpy.env.scratchWorkspace = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde")
        arcpy.Append_management(polyline, CDPRGisAdminLineasCAD, "NO_TEST","Num_Control \"NÃƒÆ’Ã‚Âºm. de Control\" true false false 10 Text 0 0 ,First,#,\\Polyline,Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#,\\Polyline,Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
        arcpy.AddMessage("polyline added")
        print("polyline added")
        arcpy.env.scratchWorkspace = TemporalEnvironment1
        arcpy.TruncateTable_management(polyline)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddMessage(e.args[0])
        
        
    #**********************************************
    #**********************************************

    #polygon ---- Polygon
    try:
        # select points from CAD
        polygono = arcpy.SelectData_management(CAD,"Polygon")#\CAD \Polyline
        print(polygono)
        
        #crear fields para el punto
        #agregar nombreCad Puntos
        arcpy.AddField_management(polygono, "Nombre_CAD","TEXT","","","50", "","NULLABLE","NON_REQUIRED","")
        print("nombreCadAgregado")
        #AgregarNumCaso
        arcpy.AddField_management(polygono, "Num_Control", "TEXT", "", "", "10", "","NULLABLE","NON_REQUIRED","")

        ##Calcular y agregar el valor a los fields creados.
        #NombreCadPuntosCalculate
        arcpy.CalculateField_management(polygono, "Nombre_CAD", "'{0}'".format(NombreCAD), "PYTHON")
        #NUmCasoPuntosCalculate
        arcpy.CalculateField_management(polygono, "Num_Control", "'{0}'".format(NumeroDeControl), "PYTHON")

##        # Process: Clear Workspace Cache
##        arcpy.ClearWorkspaceCache_management(ConexionGDB)
        
        #cargar Punto con su informacion
        TemporalEnvironment1 = arcpy.env.scratchWorkspace
        ##arcpy.env.scratchWorkspace = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde"
        arcpy.env.scratchWorkspace = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde")
        arcpy.Append_management(polygono, CDPRGisAdminPoligonosCAD, "NO_TEST","Num_Control \"NÃƒÆ’Ã‚Âºm. de Control\" true false false 10 Text 0 0 ,First,#,\\Polygon,Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#,\\Polygon,Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
        arcpy.env.scratchWorkspace = TemporalEnvironment1
        arcpy.TruncateTable_management(polygono)
        print("polygon completed")
        arcpy.AddMessage("polygon added")
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddMessage(e.args[0])
        
    return


##************************************************************
#
##                    ** Tools **
#
##************************************************************

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



##------------------------------------------------------------------------
# Main Code -- CADManagement
# Description: Main code for the CAD Management Script
##------------------------------------------------------------------------

try:
    #Workspace******
    ##  To change the direction where to send the information simply
    ## modify the following line
    ## arcpy.env.scratchWorkspace =  sys.path[0]
    try:
        print(sys.path[0])
        arcpy.AddMessage(sys.path[0])
        arcpy.env.scratchWorkspace = sys.path[0] ##Change to set workspace
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
        OutputDB = CreateDatabaseConnection(NombreVersion, instancia, v_scratchFolder)
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
        UnCompressZipCad(ArchivoComprimidoZipConCADs, cadDescomprimido)
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
    LoadCadToWeb(NumeroDeControl, cadDescomprimido, v_scratchFolder)
    arcpy.AddMessage("End of code") 
except Exception:
    ex = sys.exc_info()[1]
    print(ex.args[0])
    arcpy.AddMessage(ex.args[0])





