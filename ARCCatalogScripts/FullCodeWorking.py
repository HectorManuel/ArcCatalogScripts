# -*- ##################
# ---------------------------------------------------------------------------
# CADManagementCRIM.py coding: -*- coding: cp1252 -*-
# Usage: CADManagementCRIM <NumeroDeControl> <ArchivoComprimidoZipConCADs> <NombreVersion> 
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
# Usage: LoadCadToWeb <Numero_de_Caso> <cadDescomprimido> <ConexionGDB> <WorksapcePath>
# Description: 
# Herramienta para convertir archivos de CAD a feature class y preparlos para
# procesarlos y subirlos a geodatabase.
# ---------------------------------------------------------------------------

def LoadCadToWeb(Numero_de_Caso, cadDescomprimido, ConexionGDB, WorkspacePath):
    ##messages to guide the user through the running script
    arcpy.AddMessage("DENTRO DE LOAD CAD TO WEB")
    arcpy.AddMessage(Numero_de_Caso)
    arcpy.AddMessage(cadDescomprimido)
    arcpy.AddMessage(ConexionGDB)
    
    ### Set local variables
    ##cadDescomprimido = "c:\\ManejoCAD\\cadDescomprimido"
    ScratchGDB = arcpy.env.workspace
    CAD_StatePlane = arcpy.env.workspace + "\\CAD"
    CAD_DefPrj = arcpy.env.workspace + "\\CAD"
    CADName =""

    #*************************

    #Main functionality*****************************
    ## Path to the Unxompressed File
    arcpy.env.workspace = cadDescomprimido

    datasets = arcpy.ListDatasets("*","All")

    for data in datasets:
        print data
        ##arcpy.AddMessage(data)
        CADName = os.path.splitext(data)[0]
        print CADName
        ##arcpy.AddMessage(CADName)

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
               
               CadToGeodatabase(data, ScratchGDB, CAD_StatePlane)
               
               CalculaYCargaScript(CAD_DefPrj, CADName, Numero_de_Caso, ConexionGDB, WorkspacePath)
           elif prj == "unknown": 
               arcpy.AddMessage("To continue, first define a coordinate system!")
               print ("To continue, first define a coordinate system!")
               print(prj)
               arcpy.DefineProjection_management(data, "PROJCS['NAD_1983_StatePlane_Puerto_Rico_Virgin_Islands_FIPS_5200',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['False_Easting',200000.0],PARAMETER['False_Northing',200000.0],PARAMETER['Central_Meridian',-66.43333333333334],PARAMETER['Standard_Parallel_1',18.03333333333333],PARAMETER['Standard_Parallel_2',18.43333333333333],PARAMETER['Latitude_Of_Origin',17.83333333333333],UNIT['Meter',1.0]]")
               ##arcpy.CadToGeodatabase_CADManagement(data, ScratchGDB, CAD_StatePlane)
               CadToGeodatabase(data,ScratchGDB, CAD_StatePlane)
               ##arcpy.CalculaYCargaScript_CADManagement(CAD_DefPrj, CADName, Numero_de_Caso, ConexionGDB)
               CalculaYCargaScript(CAD_DefPrj, CADName, Numero_de_Caso, ConexionGDB. WorkspacePath)
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
# ---------------------------------------------------------------------------
# Usage: CalculaYCargaScript <CAD> <NombreCAD> <NumeroDeControl> <ConexionGDB> <WorksapcePath>
# Description: 
# Herramienta para convertir archivos de CAD a feature class y preparlos para
# procesarlos y subirlos a geodatabase.
# ---------------------------------------------------------------------------

def CalculaYCargaScript(CAD, NombreCAD, NumeroDeControl, ConexionGDB, WorkspacePath):
                        
    arcpy.AddMessage("CALCULA Y CARGA")
    arcpy.AddMessage("CAD: " + CAD)
    arcpy.AddMessage("Nombre CAD: " + NombreCAD)
    arcpy.AddMessage("Numero de Control: " + NumeroDeControl)
    arcpy.AddMessage("Conexion Geodatabase: " + ConexionGDB)

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

    ##CDPRGidAdminPuntosCAD = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde\\CDPR.GISADMIN.Puntos_CAD"
    ##
    ##CDPRGisAdminLineasCAD = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde\\CDPR.GISADMIN.Lineas_CAD"
    ##
    ##CDPRGisAdminPoligonosCAD = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde\\CDPR.GISADMIN.Poligonos_CAD"
    try:
        ##Assign the Path toe the Conection where the information will be copied
        CDPRGidAdminPuntosCAD = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde","CDPR.GISADMIN.Puntos_CAD")

        CDPRGisAdminLineasCAD = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde","CDPR.GISADMIN.Lineas_CAD")

        CDPRGisAdminPoligonosCAD = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde","CDPR.GISADMIN.Poligonos_CAD")

    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddMessage(e.args[0])
    #**********************************************
    #**********************************************
    arcpy.AddMessage("--Appending CAD Information--")

    #Puntos ---- Point
    try:
        # select points from CAD
        pointer = arcpy.SelectData_management(CAD,"Point")#\CAD \Point
        arcpy.AddMessage(pointer)
        arcpy.AddMessage("**Adding Point**")
        #create fields for the Point Shapes
        #Add Nombre_CAD field to scratch table
        arcpy.AddField_management(pointer, "Nombre_CAD","TEXT","","","50", "" ,"NULLABLE","NON_REQUIRED","")

        #Add Num_Control Field
        arcpy.AddField_management(pointer, "Num_Control", "TEXT", "", "", "10", "Núm. de Control","NULLABLE","NON_REQUIRED","")

        ##CAlculate and Add the information to the scratch table
        #Nombre_Cad 
        arcpy.CalculateField_management(pointer, "Nombre_CAD", "'{0}'".format(NombreCAD), "PYTHON", "")
        #Num_Control
        arcpy.CalculateField_management(pointer, "Num_Control", "'{0}'".format(str(NumeroDeControl)), "PYTHON", "")


        # Process: Clear Workspace Cache to avoid errors on connection or overflows and conection problems
        arcpy.ClearWorkspaceCache_management(ConexionGDB)
        arcpy.AddMessage("Workspace Cleared")

        #Load and Append the points
        TemporalEnvironment = WorkspacePath
        WorkspacePath = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde")
        ##arcpy.AddMessage(WorkspacePath)
        arcpy.Append_management(pointer, CDPRGidAdminPuntosCAD, "NO_TEST","Num_Control \"Núm. de Control\" true false false 10 Text 0 0 ,First,#," + str(pointer) + ",Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#," + str(pointer) + ",Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#", "")
        ##arcpy.Append_management(pointer, CDPRGidAdminPuntosCAD, "TEST", "", "")
        ##arcpy.Append_management(pointer, CDPRGidAdminPuntosCAD, "NO_TEST","Num_Control \"Núm. de Control\" true false false 10 Text 0 0 ,First,#,\\Point,Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#,\\Point,Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#", "")
        arcpy.AddMessage("Appended: " + CDPRGidAdminPuntosCAD)
        WorkspacePath = TemporalEnvironment
        ##arcpy.AddMessage(WorkspacePath)
        arcpy.AddMessage("Point added")
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
        arcpy.AddMessage(polyline)
        arcpy.AddMessage("**Adding Polyline**")
        #Create Fields for Polyline
        #Add Nombre_CAD field
        arcpy.AddField_management(polyline, "Nombre_CAD","TEXT","","","50", "","NULLABLE","NON_REQUIRED","")

        #Add Num_Control
        arcpy.AddField_management(polyline, "Num_Control", "TEXT", "", "", "10", "Núm. de Control","NULLABLE","NON_REQUIRED","")

        arcpy.CalculateField_management(polyline, "Nombre_CAD", "'{0}'".format(NombreCAD), "PYTHON")
        arcpy.CalculateField_management(polyline, "Num_Control", "'{0}'".format(str(NumeroDeControl)), "PYTHON")

        # Process: Clear Conection Workspace Cache
        arcpy.ClearWorkspaceCache_management(ConexionGDB)
        arcpy.AddMessage("Workspace for lines cleared")
        
        #cargar Punto con su informacion
        TemporalEnvironment1 = WorkspacePath
        ##arcpy.env.scratchWorkspace = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde"
        WorkspacePath = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde")

##        #********TEST*********
##        fieldMapping = arcpy.FieldMappings()
##        fieldMapping.addTable(CDPRGisAdminLineasCAD)
##
##        inputFields = [field.name for field in arcpy.ListFields(CDPRGisAdminLineasCAD)]
##        for inputfield in inputFields:
##            arcpy.AddMessage(inputfield)
            
        arcpy.Append_management(polyline, CDPRGisAdminLineasCAD, "NO_TEST","Num_Control \"Núm. de Control\" true false false 10 Text 0 0 ,First,#," + str(polyline) + ",Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#," + str(polyline) + ",Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")    
        ##arcpy.Append_management(polyline, CDPRGisAdminLineasCAD, "TEST", "", "")
        ##arcpy.Append_management("\\Polyline", CDPRGisAdminLineasCAD, "NO_TEST","Num_Control \"Núm. de Control\" true false false 10 Text 0 0 ,First,#,\\Polyline,Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#,\\Polyline,Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
        arcpy.AddMessage("Appended: " + CDPRGisAdminLineasCAD) 
        arcpy.AddMessage("Polyline added")
        WorkspacePath = TemporalEnvironment1
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
        arcpy.AddMessage(polygono)
        arcpy.AddMessage("**Appending Polygon**")
        #crear fields para el punto
        #agregar nombreCad Puntos
        arcpy.AddField_management(polygono, "Nombre_CAD","TEXT","","","50", "","NULLABLE","NON_REQUIRED","")
        print("nombreCadAgregado")
        #AgregarNumCaso
        arcpy.AddField_management(polygono, "Num_Control", "TEXT", "", "", "10", "Núm. de Control","NULLABLE","NON_REQUIRED","")

        ##Calcular y agregar el valor a los fields creados.
        #NombreCadPuntosCalculate
        arcpy.CalculateField_management(polygono, "Nombre_CAD", "'{0}'".format(NombreCAD), "PYTHON")
        #NUmCasoPuntosCalculate
        arcpy.CalculateField_management(polygono, "Num_Control", "'{0}'".format(str(NumeroDeControl)), "PYTHON")

        # Process: Clear Workspace Cache
        arcpy.ClearWorkspaceCache_management(ConexionGDB)
        arcpy.AddMessage("Workspace for polygons cleared")
        
        #cargar Punto con su informacion
        TemporalEnvironment2 = WorkspacePath
        ##arcpy.env.scratchWorkspace = "C:\\ManejoCAD\\scratch\\Conexion_GDB.sde"
        WorkspacePath = os.path.join(arcpy.env.scratchFolder, "Conexion_GDB.sde")

        arcpy.Append_management(polygono, CDPRGisAdminPoligonosCAD, "NO_TEST","Num_Control \"Núm. de Control\" true false false 10 Text 0 0 ,First,#," + str(polygono) + ",Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#," + str(polygono) + ",Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")    
        ##arcpy.Append_management(polygono, CDPRGisAdminPoligonosCAD, "TEST", "", "")
        ##arcpy.Append_management(polygono, CDPRGisAdminPoligonosCAD, "NO_TEST","Núm_Control \"Num. de Control\" true false false 10 Text 0 0 ,First,#,\\Polygon,Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#,\\Polygon,Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
        arcpy.AddMessage("Appended: " + CDPRGisAdminPoligonosCAD) 
        WorkspacePath = TemporalEnvironment2
        arcpy.TruncateTable_management(polygono)
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

##*****Call fucntion that will execute to Uncompress the selected file
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

##**********if the unzip file is valid, it unzips the file
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
# Create DatabaseConnection, if it exist it recreates it if no
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
    arcpy.AddMessage("Database location:")
    arcpy.AddMessage(scratchFolder)

##*******
# CAD data conversion to geodatabase format data
##*******
def CadToGeodatabase(CAD, ScratchGDB,state):
    spatial_reference = "NAD_1983_StatePlane_Puerto_Rico_Virgin_Islands_FIPS_5200"
    print("insideCadToGeo")
    try:
        #process: convert_FC-DefProj
        arcpy.CADToGeodatabase_conversion(CAD, ScratchGDB, "CAD", "1000", "")
        arcpy.AddMessage("CAD to Geodatabase conversion success")
        print("conversion Success")
    except Exception:
        print((sys.exc_info()[1]).args[0])
    return



##------------------------------------------------------------------------
# Main Code -- CADManagement
# Description: Main code for the CAD Management Script. It obtain the input
# from the user and process the information calling the necesary functions
##------------------------------------------------------------------------

try:
    #**** Global variable*****
    WorkspacePath = sys.path[0]
    #Workspace******
    ##  To change the direction where to send the information simply
    ## modify the following line
    ## arcpy.env.scratchWorkspace =  sys.path[0]
    try:
        arcpy.AddMessage(sys.path[0])
        arcpy.AddMessage("WorkspacePath :: " + WorkspacePath)
        arcpy.AddMessage("SCRATCHFOLDER:: " + arcpy.env.scratchFolder)
        ##arcpy.env.scratchWorkspace = sys.path[0] ##Change to set workspace
        ##arcpy.env.scratchWorkspace = r"c:\ManejoCAD\scratch"
        ##arcpy.env.scratchWorkspace = arcpy.env.scratchFolder
        arcpy.AddMessage("****workspace Set*****")
        ##arcpy.AddMessage(arcpy.env.scratchWorkspace)
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
        arcpy.AddMessage("numero de control: " + NumeroDeControl)
        arcpy.AddMessage("Archivo comprimido: " + ArchivoComprimidoZipConCADs)
        arcpy.AddMessage("Nombre de version" + NombreVersion)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        print("Error Buscando Variables")
        arcpy.AddMessage(e.args[0])
    #***************

    #local variables
    try:
        instancia = "gmtserver3"
        v_scratchFolder = arcpy.env.scratchFolder
        arcpy.env.workspace = arcpy.GetParameterAsText(3)
        arcpy.AddMessage("workspace: " + arcpy.env.workspace)
        ##v_scratchFolder = os.path.join(WorkspacePath,"scratch")
        print("folderScratch: " + v_scratchFolder)
        arcpy.AddMessage("folderScratch : " + v_scratchFolder)
        conexionGDBsde = v_scratchFolder
        arcpy.AddMessage("Cad descomprimido")
        cadDescomprimido = os.path.join(WorkspacePath,"cadDescomprimido")
        print(cadDescomprimido)
        arcpy.AddMessage(cadDescomprimido)
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
        arcpy.AddMessage("**Database connection created**")
        arcpy.AddMessage(OutputDB)
        print(OutputDB)
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        print("Error creando coneccion base datos")
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
    
    print("entrando a loadear loc CAD")
    ##arcpy.LoadCadToWeb_CADManagement(NumeroDeControl, cadDescomprimido, v_scratchFolder)
    LoadCadToWeb(NumeroDeControl, cadDescomprimido, v_scratchFolder, WorkspacePath)
    arcpy.AddMessage("End of code, Success")
except Exception:
    ex = sys.exc_info()[1]
    print(ex.args[0])
    arcpy.AddMessage(ex.args[0])
































































