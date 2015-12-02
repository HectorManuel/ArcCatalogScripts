# -*- coding: utf-8 -*-

#*****information*********
#calcula y carga archivo CAD
#*****************************

#libraries to import
import arcpy, os, sys

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
        arcpy.Append_management(pointer, CDPRGidAdminPuntosCAD, "NO_TEST","Num_Control \"Núm. de Control\" true false false 10 Text 0 0 ,First,#,\\Point,Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#,\\Point,Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#", "")
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
        arcpy.Append_management(polyline, CDPRGisAdminLineasCAD, "NO_TEST","Num_Control \"Núm. de Control\" true false false 10 Text 0 0 ,First,#,\\Polyline,Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#,\\Polyline,Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
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
        arcpy.Append_management(polygono, CDPRGisAdminPoligonosCAD, "NO_TEST","Num_Control \"Núm. de Control\" true false false 10 Text 0 0 ,First,#,\\Polygon,Num_Control,-1,-1;Nombre_CAD \"Nombre de CAD\" true false false 50 Text 0 0 ,First,#,\\Polygon,Nombre_CAD,-1,-1;Fecha_Creado \"Fecha_Creado\" false true false 36 Date 0 0 ,First,#;SHAPE.STArea() \"SHAPE.STArea()\" false false true 0 Double 0 0 ,First,#;SHAPE.STLength() \"SHAPE.STLength()\" false false true 0 Double 0 0 ,First,#", "")
        arcpy.env.scratchWorkspace = TemporalEnvironment1
        arcpy.TruncateTable_management(polygono)
        print("polygon completed")
        arcpy.AddMessage("polygon added")
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
        arcpy.AddMessage(e.args[0])
        
    return
