#! /usr/bin/env python
# -*- coding: utf-8 -*-

#execfile(r"C:\Users\CPR\Desktop\codigo_python_arcgis\templateArcPieCita_20170711.py")
#Se instalo la biblioteca pygresql
# PyGreSQL-4.1.1.win32-py2.6-pg8.4.msi Esta es la version que se instalo, la que funciono. En Python/Arcgis10/  No instalar en otra direccion
# En la actualizacion se instalo: PyGreSQL-4.1.1.win32-py2.7-pg8.4.msi, en el directorio: C:\\Python27\ArcGis10.3  La baje de aqui: http://www.pygresql.org/files/

#############Script que anade una capa mas############

import arcpy
from arcpy import env
import os
import pg
import subprocess
#import re
########inicia conexion base de datos y query#################

#conn = pg.connect(dbname='xxx', user='xxx', passwd='xxx', host='xxx')

########termina conexion base de datos y query#################

lista_shapes = os.listdir("C:\\Users\\CPR\\Desktop\\template\\lyr")
for shapefile in lista_shapes:

    filename, file_extension = os.path.splitext(shapefile)

    filename = filename.upper()

    consulta = "select nombre from coberturas where cobertura="+"'"+filename+"'"+""

    consulta_escala = "select escala from coberturas where cobertura="+"'"+filename+"'"+""
    consulta_publish = "select publish from coberturas where cobertura="+"'"+filename+"'"+""

    consulta_id = 'select "RECORD ID" as re from coberturas where cobertura='+"'"+filename+"'"+""

    consulta_fecha = 'select pubdate from coberturas where cobertura='+"'"+filename+"'"+""

    resultado = conn.query(consulta)
    rows = resultado.namedresult()

    titulo = rows[0].nombre

    titulo_shapeEstilo = titulo.split("(")

    titulo_shapeEstilo[0]

    titulo_shape = "<CLR red='204' green='204' blue='204'><ita>"+titulo_shapeEstilo[0]+"</ita></CLR>("+titulo_shapeEstilo[1]

    cita_shape = "<ita>"+titulo_shapeEstilo[0]+"</ita>("+titulo_shapeEstilo[1]

    titulo_shape = titulo_shape.replace("Distribución potencial", "")
    titulo_shape = titulo_shape.replace("Sitios de recolecta", "")

    resultado_escala = conn.query(consulta_escala)
    rows_escala = resultado_escala.namedresult()
    escala_query = rows_escala[0].escala

    resultado_publish = conn.query(consulta_publish)
    rows_publish = resultado_publish.namedresult()
    publish_query = rows_publish[0].publish

    resultado_fecha = conn.query(consulta_fecha)
    rows_fecha = resultado_fecha.namedresult()
    fecha_query = rows_fecha[0].pubdate

    fecha = fecha_query.split('/')

    resultado_id = conn.query(consulta_id)
    rows_record_id = resultado_id.namedresult()
    record_query = rows_record_id[0].re

    record_query = str(record_query)

    autores = 'select origin from "Autores_origen" where "ID_origen"='+record_query+''
    resultado_id = conn.query(autores)
    autores_id = resultado_id.namedresult()

    if len(autores_id) > 0:
        autores_query = autores_id[len(autores_id)-1].origin
    elif len(autores_id) == 0:
        autores_query = "Autor"
    else:
        autores_query = autores_id[0].origin

    cita = autores_query+". "+fecha[2]+". "+cita_shape+". "+escala_query+". "+publish_query 

    cita1 = autores_query+". "+fecha[2]+". "+cita_shape+". "+escala_query+". " 
    cita2 = publish_query 

    mxd = arcpy.mapping.MapDocument(r"C:\\Users\\CPR\\Desktop\\template\\base\\baseA.mxd")
    mxd_P = arcpy.mapping.MapDocument(r"C:\\Users\\CPR\\Desktop\\template\\base\\puntosA.mxd")

    df = arcpy.mapping.ListDataFrames(mxd)[0]
    df_P = arcpy.mapping.ListDataFrames(mxd_P)[0]
    
    newlayer1 = arcpy.mapping.Layer(r"C:\\Users\\CPR\\Desktop\\template\\shp\\"+shapefile+"")

    desc = arcpy.Describe(r"C:\\Users\\CPR\\Desktop\\template\\shp\\"+shapefile+"")

    #print desc.shapeType 
    #print desc.featureType
    #print desc.datasetType
    print "Trabajando "+desc.file+". Espera por favor." 
    #print desc.dataElementType
    #print desc.baseName

    if desc.shapeType == "Polygon":

        symbologyLayer = (r"C:\\Users\\CPR\\Desktop\\template\\base\\baseNew.lyr")
        arcpy.ApplySymbologyFromLayer_management(newlayer1, symbologyLayer)
        arcpy.mapping.AddLayer(df, newlayer1, "AUTO_ARRANGE")

        for capa in arcpy.mapping.ListLayers(mxd, "", df):

            if capa.name == "dest_2010gw": 
                oldlayer = capa
            if capa.name == desc.baseName:
                newLayer = capa
        
        arcpy.mapping.MoveLayer(df, newLayer, oldlayer,  "BEFORE")

        ext = newlayer1.getExtent()

        df.extent = ext

        for elm in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
            if elm.text == 'titulo':
                elm.text = titulo_shape

        for elmPie in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
            if elmPie.text == 'cita1':
                elmPie.text = cita1

        for elmPie in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
            if elmPie.text == 'cita2':
                elmPie.text = cita2

#    arcpy.RefreshActiveView()
#    arcpy.RefreshTOC()

        for img in arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT"):

            img.sourceImage = (r"C:\\Users\\CPR\\Desktop\\tempalte\\fb\\"+filename+".jpg")
            img.elementPositionX = 0.5082
            img.elementPositionY = 11.17
            img.elementWidth = 4.1117
    
        logo = arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT")[0]

        logo.sourceImage = (r"C:\\Users\\CPR\\Desktop\\template\\base\\logo2012_2018.PNG")
        logo.elementPositionX = 0.5006
        logo.elementPositionY = 19.060
        logo.elementWidth = 2.0395
        logo.elementHeight = 2.02

        cc = arcpy.mapping.ListLayoutElements(mxd, "PICTURE_ELEMENT")[2]
    
        cc.sourceImage = (r"C:\\Users\\CPR\\Desktop\\cc.png")
        cc.elementPositionX = 24.44
        cc.elementPositionY = 0.6
        cc.elementWidth = 2.85
        cc.elementHeight = 0.99

        mxd.saveACopy(r"C:\\Users\\CPR\\Desktop\\template\\mxd\\"+filename+".mxd")

        arcpy.mapping.ExportToPNG(mxd, r"C:\\Users\\CPR\\Desktop\\template\\png\\"+filename+".png", resolution=300)
    
        for df in arcpy.mapping.ListDataFrames(mxd):
            for lyr in arcpy.mapping.ListLayers(mxd, "", df):
                if lyr.name == filename:        
                    arcpy.mapping.RemoveLayer(df, lyr)

        for elemento in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
            if elemento.text == titulo_shape.decode('utf-8'):
                elemento.text = 'titulo'

        for elementoPie in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
            if elementoPie.text == cita1.decode('utf-8'):
                elementoPie.text = 'cita1'

        for elementoPie in arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT"):
            if elementoPie.text == cita2.decode('utf-8'):
                elementoPie.text = 'cit2'

    else:

        symbologyLayer = (r"C:\\Users\\CPR\\Desktop\\template\\base\\basePuntos.lyr")

        arcpy.ApplySymbologyFromLayer_management(newlayer1, symbologyLayer)
        arcpy.mapping.AddLayer(df_P, newlayer1, "AUTO_ARRANGE")

        ext = newlayer1.getExtent()

        df_P.extent = ext

        for elm in arcpy.mapping.ListLayoutElements(mxd_P, "TEXT_ELEMENT"):
            if elm.text == 'titulo':
                elm.text = titulo_shape

        for elmPie in arcpy.mapping.ListLayoutElements(mxd_P, "TEXT_ELEMENT"):
            if elmPie.text == 'cita1':
                elmPie.text = cita1

        for elmPie in arcpy.mapping.ListLayoutElements(mxd_P, "TEXT_ELEMENT"):
            if elmPie.text == 'cita2':
                elmPie.text = cita2

#    arcpy.RefreshActiveView()
#    arcpy.RefreshTOC()

        for img in arcpy.mapping.ListLayoutElements(mxd_P, "PICTURE_ELEMENT"):
            img.sourceImage = (r"C:\\Users\\CPR\\Desktop\\tempalte\\fb\\"+filename+".jpg")
            img.elementPositionX = 0.5082
            img.elementPositionY = 11.174
            img.elementWidth = 4.1117
    
        logo = arcpy.mapping.ListLayoutElements(mxd_P, "PICTURE_ELEMENT")[0]

        logo.sourceImage = (r"C:\\Users\\CPR\\Desktop\\template\\base\\logo2012_2018.PNG")
        logo.elementPositionX = 0.5006
        logo.elementPositionY = 19.060
        logo.elementWidth = 2.0395
        logo.elementHeight = 2.02

        cc = arcpy.mapping.ListLayoutElements(mxd_P, "PICTURE_ELEMENT")[2]
    
        cc.sourceImage = (r"C:\\Users\\CPR\\Desktop\\cc.png")
        cc.elementPositionX = 24.44
        cc.elementPositionY = 0.6
        cc.elementWidth = 2.85
        cc.elementHeight = 0.99

        mxd_P.saveACopy(r"C:\\Users\\CPR\\Desktop\\template\\mxd\\"+filename+".mxd")

        arcpy.mapping.ExportToPNG(mxd_P, r"C:\\Users\\CPR\\Desktop\\template\\png\\"+filename+".png", resolution=300)
        for df_P in arcpy.mapping.ListDataFrames(mxd_P):
            for lyr in arcpy.mapping.ListLayers(mxd_P, "", df_P):
                if lyr.name == filename:        
                    arcpy.mapping.RemoveLayer(df_P, lyr)

        for elemento in arcpy.mapping.ListLayoutElements(mxd_P, "TEXT_ELEMENT"):
            if elemento.text == titulo_shape.decode('utf-8'):
                elemento.text = 'titulo'

        for elementoPie in arcpy.mapping.ListLayoutElements(mxd_P, "TEXT_ELEMENT"):
            if elementoPie.text == cita1.decode('utf-8'):
                elementoPie.text = 'cita1'

        for elementoPie in arcpy.mapping.ListLayoutElements(mxd_P, "TEXT_ELEMENT"):
            if elementoPie.text == cita2.decode('utf-8'):
                elementoPie.text = 'cita2'

################Fin script que anade una capa mas######################

conn.close()
