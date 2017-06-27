#! /usr/bin/env python
# -*- coding: utf-8 -*-


#execfile(r"C:\Users\CPR\Desktop\codigo_python_arcgis\templateArcPy.py")
#Se instalo la biblioteca pygresql
# PyGreSQL-4.1.1.win32-py2.6-pg8.4.msi Esta es la version que se instalo, la que funciono. En Python/Arcgis10/  No instalar en otra direccion
# En la actualizacion se instalo: PyGreSQL-4.1.1.win32-py2.7-pg8.4.msi, en el directorio: C:\\Python27\ArcGis10.3  La baje de aqui: http://www.pygresql.org/files/


#############Script que anade una capa mas############

import arcpy
from arcpy import env
import os
import pg
import subprocess

########inicia conexion base de datos y query#################

conn = pg.connect(dbname='xxxx', user='xxxx', passwd='xxxxx', host='xxxxx')




########termina conexion base de datos y query#################


lista_shapes = os.listdir("C:\\Users\\CPR\\Desktop\\SHP\\shapes")

for shapefile in lista_shapes:

    filename, file_extension = os.path.splitext(shapefile)

    consulta = "select nombre from coberturas where cobertura="+"'"+filename+"'"+""
    resultado = conn.query(consulta)
    rows = resultado.namedresult()

    titulo_shape = rows[0].nombre

    mxd = arcpy.mapping.MapDocument(r"C:\\Users\\CPR\\Desktop\\SHP\\base.mxd")

    df = arcpy.mapping.ListDataFrames(mxd)[0]
    
    newlayer1 = arcpy.mapping.Layer(r"C:\\Users\\CPR\\Desktop\\SHP\\capas\\"+shapefile+"")

    symbologyLayer = (r"C:\\Users\\CPR\\Desktop\\SHP\\capas\\shp_base.lyr")

    arcpy.ApplySymbologyFromLayer_management(newlayer1, symbologyLayer)
    arcpy.mapping.AddLayer(df, newlayer1, "AUTO_ARRANGE")


    ext = newlayer1.getExtent()

#ext = lyr.getSelectedExtent()

    df.extent = ext





    for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elm.text == 'titulo':
            elm.text = titulo_shape


#    arcpy.RefreshActiveView()
#    arcpy.RefreshTOC()



        



    for img in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):
    
    
        img.sourceImage = (r"C:\\Users\\CPR\\Desktop\\SHP\\fotos\\"+filename+".jpg")
        img.elementPositionX = 0.50
        img.elementPositionY = 10.68
        img.elementWidth = 4.11
        img.elementHeight = 2.71
        
    


    
    logo = arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT")[0]


    logo.sourceImage = (r"C:\\Users\\CPR\\Desktop\\logo2012_2018.PNG")
    logo.elementPositionX = 0.5
    logo.elementPositionY = 19.06
    logo.elementWidth = 2
    logo.elementHeight = 1.98



    cc = arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT")[2]
    
    cc.sourceImage = (r"C:\\Users\\CPR\\Desktop\\cc.png")
    cc.elementPositionX = 24.44
    cc.elementPositionY = 0.6
    cc.elementWidth = 2.85
    cc.elementHeight = 0.99
        


    

    mxd.saveACopy(r"C:\\Users\\CPR\\Desktop\\SHP\\mxds\\"+filename+".mxd")
    
    

    arcpy.mapping.ExportToPNG(mxd, r"C:\\Users\\CPR\\Desktop\\SHP\\images\\"+filename+".png")
    #arcpy.mapping.ExportToPNG(mxd, r"C:\\Users\\CPR\\Desktop\\SHP\\images\\"+filename+".png")    
    #arcpy.mapping.ExportToPNG(mxd, r"C:\\Users\\CPR\\Desktop\\SHP\\images\\"+filename+".png",df,df_export_width=1600, df_export_height=1200, world_file=True)
    #arcpy.RefreshActiveView() 
    #arcpy.RefreshTOC()
    #ruta = "r"+"\'"+"C:\Users\CPR\Desktop\SHP\images\\"+filename+".png"+"\'"
    #print ruta
    #arcpy.mapping.ExportToPNG(mxd, r"C:\\Users\\CPR\\Desktop\\SHP\\images\\"+filename+".png")
    #arcpy.mapping.ExportToPNG(mxd, r"\'"+"C:\Users\CPR\Desktop\SHP\images\\"+filename+".png"+"\'")
    
    for df in arcpy.mapping.ListDataFrames(mxd):
         for lyr in arcpy.mapping.ListLayers(mxd, "", df):
            if lyr.name == filename:        
                arcpy.mapping.RemoveLayer(df, lyr)


    for elemento in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
        if elemento.text == titulo_shape.decode('utf-8'):
            elemento.text = 'titulo'

################Fin script que anade una capa mas######################

conn.close()

