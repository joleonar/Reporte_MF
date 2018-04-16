# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 13:32:39 2016
Crea las tablas en formato latex que se agregarán al achivo Latex que genera
el Reporte de Mecanismo Focal, el contenido de las tablas creadas es el 
sigueinte:
tabla1.tex : Fecha y Tiempo Origen UTC/Local, Localizacion hipocentral
tabla2.tex : Distancias a los poblados mas cercanos y su ubicacion relativa 
tabla3.tex : Parametros del mecanismo focal Planos y Tensores
@author: lalvarado
"""

import re
import pytz, datetime

# Extra datos del archivo focmec.dat
fname = "focmec.dat"
fh = open(fname)

for line in fh:
    line=line.rstrip()
    if re.match('^  20',line):
        year  = int(line[2:6])
        month = int(line[7:9])
        day =  int(line[9:11])
        hh = int(line[12:14])
        mm = int(line[14:16])
        ss = float(line[17:21])
        lat = float(line[25:32])
        lon = float(line[32:40])
        depth = float(line[39:44])
        mag = float(line[57:60])

Tiempo_UTC = str(year)+'-'+ str(month)+'-'+str(day)+' '+str(hh)+':'+str(mm)+':'+ str(int(round(ss,0)))
#fecha_sismo = time.strptime(fecha_hora, "%Y %m %d %H %M %S")


# Crea tabla1.tex
local = pytz.timezone ("Etc/GMT-4")
naive = datetime.datetime.strptime (Tiempo_UTC, "%Y-%m-%d %H:%M:%S")
local_dt = local.localize(naive, is_dst=None)
utc_dt = local_dt.astimezone (pytz.utc)

T_UTC=naive.strftime("%Y-%m-%d %H:%M:%S") #Tiempo UTC en formato tiempo
TL=utc_dt.strftime("%Y-%m-%d %H:%M:%S")   #Tiempo Local en formato tiempo

ft_nf =open('filename.txt','w')
ft_nf.write(T_UTC[0:4]+T_UTC[5:7]+T_UTC[8:10]+'_'+T_UTC[11:13]+T_UTC[14:16])
ft_nf.close()

ft1 = open('tabla1.tex','w')
ft1.write('\\begin{multicols}{2}\n')
ft1.write('\\begin{large}')
ft1.write('\\begin{flushright}\n')
#ft1.write('\\textsf{Fecha (UTC): \\textbf{'+ str(day)+'/'+str(month)+'/'+str(year)+'}\\vspace{0.1cm} \\\\ \n')
#ft1.write('Tiempo de Origen (UTC): \\textbf{'+str(hh)+':'+str(mm)+':'+str(int(round(ss,0)))+'} \\vspace{0.1cm} \\\\ \n')

ft1.write('\\textsf{Fecha (UTC): \\textbf{'+ T_UTC[8:10]+'/'+T_UTC[5:7]+'/'+T_UTC[0:4]+'} \\vspace{0.1cm} \\\\ \n')
ft1.write('Tiempo de Origen (UTC): \\textbf{'+T_UTC[11:]+'} \\vspace{0.1cm} \\\\ \n')

ft1.write('Fecha (HLV): \\textbf{'+ TL[8:10]+'/'+TL[5:7]+'/'+TL[0:4]+'} \\vspace{0.1cm} \\\\ \n')
ft1.write('Tiempo de Origen (HLV): \\textbf{'+TL[11:]+'} } \n')
ft1.write('\end{flushright}\n')
ft1.write('\\begin{flushleft}\n')
ft1.write('\\textsf{Latitud (\\textdegree N):  \\textbf{'+str(lat)+'} \\vspace{0.1cm} \\\\ \n')
ft1.write('Longitud (\\textdegree O): \\textbf{'+str(-round(lon,2))+'} \\vspace{0.1cm} \\\\ \n')
ft1.write('Profundidad (Km): \\textbf{' +str(depth)+'} \\vspace{0.1cm} \\\\ \n')
ft1.write('Magnitud (Mw): \\textbf{'+str(mag)+'}}  \\\\ \n')
ft1.write('\\end{flushleft}\n')
ft1.write('\\end{large}')
ft1.write('\\end{multicols}\n')
ft1.close()


# Crea tabla2.tex
from city_cercanas import city_cercanas

ciu1 = city_cercanas(lat,lon,'c1r.txt')
ciu2 = city_cercanas(lat,lon,'c2r.txt')
ciu = [ciu1,ciu2]
newc = sorted(ciu, key=lambda k: k['distancia']) 

cadena1 = str(newc[0]['distancia'])+',Km al '+ newc[0]['ubic']+ ' de '+ newc[0]['name']
cadena2 = str(newc[1]['distancia'])+',Km al '+ newc[1]['ubic']+ ' de '+ newc[1]['name']

ft2 = open('tabla2.tex','w')
ft2.write('\\begin{center}\n')
ft2.write('\\textsf{\small{\n')
ft2.write('\\begin{tabular}{llll}\n')
ft2.write("\\multicolumn{2}{l}{LOCALIZACI\\'ON EPICENTRAL}& \\multicolumn{2}{l}{"+cadena1+'}\\\\ \n')
ft2.write('\\multicolumn{2}{l}{}& \multicolumn{2}{l}{ '+ cadena2 +'}\\\\ \n')
ft2.write('\\end{tabular} \n')
ft2.write('}} \n') 
ft2.write('\\end{center} \n')
ft2.close()

fhplt=open('FOCO1.PLT')
for line2 in fhplt:
    line2=line2.rstrip()
    if re.search('A:',line2):
        A = line2[30:48]
    if re.search('B:',line2):
        B = line2[30:48]
    if re.search('T:',line2):
        T = line2[27:48]
    if re.search('"P:',line2):
        P = line2[27:48]
        

ft3 = open('tabla3.tex','w')
ft3.write('\\begin{tabular}{llll}\n')
ft3.write('& {\\small Azimuth (\\textdegree)} & {\\small Buzamiento (\\textdegree)} &{\\small Deslizamiento (\\textdegree)}\\\\ \n')
ft3.write('\\midrule \\vspace{0.1cm}\n')
ft3.write('\\bf{A}   & '+  A[0:5]+'   & ' +A[7:11] + ' & '+ A[12:] +' \\\\ \n')
ft3.write('\\bf{B}   & '+  B[0:5]+'   & ' +B[7:11] + ' & '+ B[12:] +' \\\\ \n')
ft3.write('   &            &                &                 \\\\ \n' )
ft3.write(" & {\\small Orientaci\\'on({\\textdegree})} &{\small Inclinaci\\'on(\\textdegree)} &   \\\\ \n" )
ft3.write('\\midrule \\vspace{0.1cm}\n')
ft3.write('\\bf{T}  & '+ T[2:8]+' & '+ T[9:-1]+' &  \\\\ \n ')
ft3.write('\\bf{P}  & '+ P[2:8]+' & '+ P[9:-1]+' &  \\\\ \n ')
ft3.write('\\end{tabular}\n')
ft3.close()

