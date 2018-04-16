# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 08:39:27 2016
Funcion para identificar la ciudad mas cercana al epicentro de un listado de 
ciudades (c1r.txt ó c2r.txt),ademas de la distancia  tambien se determina
el azimuth, ubicacion relativa y nombre de la ciudad
@author: lalvarado
"""
def city_cercanas(lat,lon,file_in):
    
    from pygc import great_distance
    from geopy.distance import great_circle
    import pandas as pd
    import numpy as np
    
    # Lee los archivos de las ciudades
    c1r_df = pd.read_table(file_in, sep=':',header=None,low_memory=False)
   
    c1r_df.columns = ['Lat1', 'Lon1', 'City'] # Da nombre a las columnas

    
    p = (lat,lon) # tupla con coord del epicentro
    p1 =zip(c1r_df.Lat1,c1r_df.Lon1) #Lista de tuplas con las coordenadas de ciudades
   
    D1 = [great_circle(p,c).kilometers for c in p1 ] # Distancia  epi a c/ciudad

    dist1=np.array(D1)
    ind1= dist1.argmin()
    
     # Crea diccionario  par cada ciudad {'name':  , 'distanca': }
    ciudad1 = {'name': c1r_df.City[ind1],'distancia':int(round(dist1[ind1],0))}
   
    latc1=c1r_df.Lat1[ind1]
    lonc1=c1r_df.Lon1[ind1]

    res1=great_distance(start_latitude=latc1, start_longitude=lonc1, end_latitude=lat, end_longitude=lon)

    ciudad1['azimuth']=round(res1['azimuth'],1)
    
    def ubicacion(azimuth):  #Funcion para determina ubicacion
        if azimuth <= 15: ubic='norte'
        elif (azimuth > 15) & (azimuth <= 75): ubic='noreste'
        elif (azimuth > 75) & (azimuth <=105): ubic='este'
        elif (azimuth >105) & (azimuth <=165): ubic='sureste'
        elif (azimuth >165) & (azimuth <=195): ubic='sur'
        elif (azimuth >195) & (azimuth <=255): ubic='suroeste'
        elif (azimuth >255) & (azimuth <=285): ubic='oeste'
        elif (azimuth >285) & (azimuth <=345): ubic='noroeste'
        elif azimuth > 345: ubic='norte'
        
        return ubic
     
    ciudad1['ubic'] = ubicacion(res1['azimuth'])
    
    print 'A ', ciudad1['distancia'] ,'Km al ', ciudad1['ubic'],'de', ciudad1['name']
    
    return ciudad1; 
