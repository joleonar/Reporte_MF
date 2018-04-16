# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 10:40:30 2016

@author: lalvarado
"""

import re

# Extra datos del archivo focmec.dat
fname = "focmec.dat"

fh = open(fname)
#fout = 'foco1.pol'
#fs = open(fout,'w')
#fout2 = 'mf.txt'
#fs2 = open(fout2,'w')

#fs2.write('stat'), fs2.write(' '), fs2.write('azim'),fs2.write(' '),fs2.write('ih'),
#fs2.write(' '),fs2.write('pol'),fs2.write('\r\n')


from polar_change import focmec2focopol
focmec2focopol()

from polar_change import extrae_pol
extrae_pol()





fout3 = 'reporte.sh'
fs3 = open(fout3,'w')

fout4 = 'mfbb.txt'
fs4 = open(fout4,'w')

fout5 = 'mfbb2.txt'
fs5 = open(fout5,'w')


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
        depth = float(line[40:44])
        mag = float(line[57:60])
    
    
    #if re.match('^[A-Z]',line):
    #    #print line[0:20], line[20:21]
    #    #fs.write('  '),fs.write(line[0:20]),fs.write(' '),fs.write(line[20:21]),fs.write('\r\n')
    #    fs2.write(line[0:20]),fs2.write(' '),fs2.write(line[20:21]),fs2.write('\r\n')

fs4.write('lon lat depth  str dip slip  st dip slip mant exp plon plat\n')
fs4.write(str(lon)+' '+str(lat)+' '+str(depth)+' ')

fs5.write('lon lat depth  str dip slip  st dip slip mant exp plon plat\n')
fs5.write(str(lon)+' '+str(lat)+' '+str(depth)+' ')

fhplt=open('FOCO1.PLT')
for line2 in fhplt:
    line2=line2.rstrip()
    if re.search('A:',line2):
        fs4.write(line2[30:48]+' ')
        fs5.write(line2[30:48]+' ')
    if re.search('B:',line2):
        fs4.write(line2[30:48]+' ')
        fs5.write(line2[30:48]+' ')
    #if re.search('T:',line):
    #    print line[27:48]
    #if re.search('P:',line):
    #    print line[27:48]

fs4.write('5.5  0 '+ str(lon+0.2) +' '+str(lat+0.2)+'\n')
fs5.write('30.0  0 '+ str(lon+0.2) +' '+str(lat+0.2)+'\n')
#TimeOrig = datetime.datetime(year,month,day,hh,mm,int(ss))
#print TimeOrig
#print lat, lon
# Coordenadas para la elaboracion del mapa 
latmin=lat-1; latmax=lat+1; lonmin=lon-1.5;lonmax=lon+1.5
fs3.write('#!/bin/bash\n')
fs3.write('gmtset DIR_GSHHG /opt/gmt5/gshhg-gmt-2.3.2\n')
fs3.write('gmtset PS_CHAR_ENCODING Standard+\n')
fs3.write('gmtset FORMAT_GEO_MAP=dddF\n')
fs3.write('gmtset MAP_FRAME_AXES WenS\n')
fs3.write('gmtset FONT_ANNOT_PRIMARY 8\n') 
fs3.write('ps="reporte.ps"\n')
fs3.write('r="'+str(lonmin)+'/'+str(lonmax)+'/'+str(latmin)+'/'+str(latmax)+'/"\n\n')
fs3.write('psbasemap -R$r -Jm4.0 -Ba1 -X1.8 -P -Y6.7 -K > $ps\n')
fs3.write('grdimage etopo1_bedrock.grd -R -J -Cverde.cpt -E50 -O -K >> $ps\n')
fs3.write('pscoast -Jm -R -Df -C195/255/255  -N1/2 -I2/0.25p,deepskyblue4 -I3/0.25,deepskyblue4 -Bg500 -K -O >> $ps\n')
fs3.write('pscoast -R -Jm -W -N1 -Df -T'+str(lonmin+0.300)+'/'+str(latmax-0.5)+'/2.0/1.0 -L'+str(lon)+'/'+str(latmin+0.3)+'/'+str(latmin+0.3)+'/50 -O -K >> $ps\n\n')
##-T-71.567/11.792/2.0/1.0
fs3.write('psxy fallas2015.txt -Jm -R -W0.85p,red3  -K -O >> $ps\n')
fs3.write("gawk -F: '{print $2, $1}' ciu.txt | psxy -Jm -R -Sc0.08 -G0 -L -K -O >> $ps\n")
fs3.write("gawk -F: '{print $2, $1}' ciuc.txt | psxy -Jm -R -Sc0.16 -G0 -L -K -O >> $ps\n")
fs3.write("gawk -F: '{print $5, $4-0.080, $3}' ciu.txt | pstext -Jm -R -F+f6p,Helvetica -K -O >>$ps\n")
fs3.write("gawk -F: '{print $5, $4-0.075, $3}' ciuc.txt | pstext -Jm -R -F+f8p,Helvetica-Bold,grey -K -O >> $ps\n")
fs3.write("gawk -F: '{print $5, $4-0.080, $3}' ciuc.txt | pstext -Jm -R -F+f8p,Helvetica-Bold -K -O >> $ps\n\n")

fs3.write("gawk  '{print $3, $2}' ESTACIONES.txt | psxy -Jm -R -St0.30 -Gyellow -W1 -L -K -O >> $ps\n")
fs3.write('echo -63.00  11.65  MAR CARIBE | pstext -Jm -R -F+f11p,Helvetica-Oblique,deepskyblue2 -K -O >> $ps\n')
fs3.write('echo -61.30  10.90   TRINIDAD | pstext -Jm -R -F+f10p,Helvetica-Oblique,deepskyblue2 -K -O >> $ps\n\n')

fs3.write('echo '+ str(lon)+' '+str(lat)+' | psxy -Jm -R -Gorangered -Sa0.5 -L -W1 -K -O >> $ps\n')
fs3.write('more mfbb.txt | psmeca -R -Jm -Sc1.0 -h1 -O -K -W -C >> $ps\n')

fs3.write('####  CUADRO DE LEYENDA\n')
fs3.write('echo '+ str(lonmax)+' '+ str(latmax)+' > cua.tmp\n')
fs3.write('echo '+ str(lonmax-0.550)+' '+ str(latmax)+' >> cua.tmp\n')
fs3.write('echo '+ str(lonmax-0.550)+' '+ str(latmax-0.50)+' >>  cua.tmp\n')
fs3.write('echo '+ str(lonmax)+' '+ str(latmax-0.50)+' >> cua.tmp\n')

fs3.write('psxy cua.tmp -R -Jm -Gwhite -O -K -W1 >> $ps\n')
fs3.write('rm cua.tmp\n\n')

fs3.write('echo '+ str(lonmax-0.300)+' '+str(latmax-0.055) +' LEYENDA | pstext -Jm -R -F+f8p,Helvetica-BoldOblique,black -K -O >> $ps\n')
fs3.write('echo '+ str(lonmax-0.485)+' '+str(latmax-0.160) +' | psxy -Jm -R -Sa0.3 -Gred -W0.8 -L -K -O >> $ps\n')
fs3.write('echo '+ str(lonmax-0.395)+' '+str(latmax-0.160) +' Epicentro | pstext -Jm -R -F+jLM+f7p,Helvetica-Bold -K -O  >> $ps\n')
fs3.write('echo '+ str(lonmax-0.485)+' '+str(latmax-0.260) + ' | psxy -Jm -R -Sc0.20 -G0 -W1 -L -K -O >> $ps\n')
fs3.write('echo '+ str(lonmax-0.395)+' '+str(latmax-0.260) + ' Ciudades | pstext -Jm -R -F+jLM+f7p,Helvetica-Bold -K -O >> $ps\n')
fs3.write('echo '+ str(lonmax-0.485)+' '+str(latmax-0.360) + ' | psxy -Jm -R -St0.3 -Gyellow -W1 -L -K -O >> $ps\n')
fs3.write('echo '+ str(lonmax-0.395)+' '+str(latmax-0.360) + ' Estaciones | pstext -Jm -R -F+jLM+f7p,Helvetica-Bold -K -O >> $ps\n')
fs3.write('echo '+ str(lonmax-0.525)+' '+str(latmax-0.450) + ' > leg.tmp\n') 
fs3.write('echo '+ str(lonmax-0.455)+' '+str(latmax-0.450) + ' >> leg.tmp\n') 
fs3.write('psxy leg.tmp -Jm -R -Gred -W1,red -L -K -O >> $ps\n')
fs3.write('rm leg.tmp\n')
fs3.write('echo '+ str(lonmax-0.395)+' '+str(latmax-0.450) + ' Fallas geol. | pstext -Jm -R -F+jLM+f7p,Helvetica-Bold,black -O -K >> $ps\n\n')


fs3.write('### CUADRO MECANISMO FOCAL\n')
fs3.write('echo '+ str(lonmax-0.09) + ' '+ str(latmin-0.125) + ' |psxy -R -Jm -Ss9.0 -W1/0 -G255 -O -K -N >>$ps\n')
fs3.write('more mfbb2.txt | psmeca -R -Jm -Sc1.05 -h1 -O -W -T -K -X+5.65 -Y-4.55 >> $ps\n')
fs3.write('more mf.txt | pspolar -R -Jm -N -D'+str(lon)+'/'+str(lat)+' -Sc0.2 -h1 -Qe -M6.3 -O -K -V >> $ps\n')
fs3.write('echo  '+str(lon-0.51)+' '+str(lat-0.66)+' 2.2 0.9 |psxy -R -Jm -Sr -W -G255 -O -K -N >> $ps\n')
fs3.write('echo '+str(lon-0.75)+' '+str(lat-0.62)+' | psxy -Jm -R -Sc0.18 -G0 -L -K -O -W -N >> $ps\n')
fs3.write('echo  '+str(lon-0.69)+' '+str(lat-0.62)+ ' Compresi'+'"\360"'+'n | pstext -Jm -R -F+jLM+f8p,Helvetica-Bold -K -O  >> $ps\n')
fs3.write('echo '+str(lon-0.75)+' '+str(lat-0.71)+' | psxy -Jm -R -Sc0.18 -G255 -L -K -O -W -N >> $ps\n')
fs3.write('echo '+str(lon-0.69)+' '+str(lat-0.71)+  ' Dilataci"\360"n | pstext -Jm -R -F+jLM+f8p,Helvetica-Bold -O -K >> $ps\n\n')

fs3.write('### MAPA DE REFERENCIA\n')
fs3.write('grdimage etopo1_bedrock.grd -R-74/-58/1/13 -Jm0.23 -X-5.7 -Y4.5 -Cverde.cpt -E150 -O -K >> $ps\n')
fs3.write('pscoast -Jm0.23 -R -Di -N1/1p -I1 -O -K -B500wnse -Wthinnest >> $ps\n')
fs3.write('echo '+str(lon) + ' '+str(lat)+' |psxy -R -Jm -Ss1.0 -W1,red -O  >>$ps\n')


fs3.write('ps2eps -f $ps')


fs3.close()
fs4.close()
fs5.close()



