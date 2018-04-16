#!/bin/bash
gmtset DIR_GSHHG /opt/gmt5/gshhg-gmt-2.3.2
gmtset PS_CHAR_ENCODING Standard+
gmtset FORMAT_GEO_MAP=dddF
gmtset MAP_FRAME_AXES WenS
gmtset FONT_ANNOT_PRIMARY 8
ps="reporte.ps"
r="-73.277/-70.277/7.229/9.229/"

psbasemap -R$r -Jm4.0 -Ba1 -X1.8 -P -Y6.7 -K > $ps
grdimage etopo1_bedrock.grd -R -J -Cverde.cpt -E50 -O -K >> $ps
pscoast -Jm -R -Df -C195/255/255  -N1/2 -I2/0.25p,deepskyblue4 -I3/0.25,deepskyblue4 -Bg500 -K -O >> $ps
pscoast -R -Jm -W -N1 -Df -T-72.977/8.729/2.0/1.0 -L-71.777/7.529/7.529/50 -O -K >> $ps

psxy fallas2015.txt -Jm -R -W0.85p,red3  -K -O >> $ps
gawk -F: '{print $2, $1}' ciu.txt | psxy -Jm -R -Sc0.08 -G0 -L -K -O >> $ps
gawk -F: '{print $2, $1}' ciuc.txt | psxy -Jm -R -Sc0.16 -G0 -L -K -O >> $ps
gawk -F: '{print $5, $4-0.080, $3}' ciu.txt | pstext -Jm -R -F+f6p,Helvetica -K -O >>$ps
gawk -F: '{print $5, $4-0.075, $3}' ciuc.txt | pstext -Jm -R -F+f8p,Helvetica-Bold,grey -K -O >> $ps
gawk -F: '{print $5, $4-0.080, $3}' ciuc.txt | pstext -Jm -R -F+f8p,Helvetica-Bold -K -O >> $ps

gawk  '{print $3, $2}' ESTACIONES.txt | psxy -Jm -R -St0.30 -Gyellow -W1 -L -K -O >> $ps
echo -63.00  11.65  MAR CARIBE | pstext -Jm -R -F+f11p,Helvetica-Oblique,deepskyblue2 -K -O >> $ps
echo -61.30  10.90   TRINIDAD | pstext -Jm -R -F+f10p,Helvetica-Oblique,deepskyblue2 -K -O >> $ps

echo -71.777 8.229 | psxy -Jm -R -Gorangered -Sa0.5 -L -W1 -K -O >> $ps
more mfbb.txt | psmeca -R -Jm -Sc1.0 -h1 -O -K -W -C >> $ps
####  CUADRO DE LEYENDA
echo -70.277 9.229 > cua.tmp
echo -70.827 9.229 >> cua.tmp
echo -70.827 8.729 >>  cua.tmp
echo -70.277 8.729 >> cua.tmp
psxy cua.tmp -R -Jm -Gwhite -O -K -W1 >> $ps
rm cua.tmp

echo -70.577 9.174 LEYENDA | pstext -Jm -R -F+f8p,Helvetica-BoldOblique,black -K -O >> $ps
echo -70.762 9.069 | psxy -Jm -R -Sa0.3 -Gred -W0.8 -L -K -O >> $ps
echo -70.672 9.069 Epicentro | pstext -Jm -R -F+jLM+f7p,Helvetica-Bold -K -O  >> $ps
echo -70.762 8.969 | psxy -Jm -R -Sc0.20 -G0 -W1 -L -K -O >> $ps
echo -70.672 8.969 Ciudades | pstext -Jm -R -F+jLM+f7p,Helvetica-Bold -K -O >> $ps
echo -70.762 8.869 | psxy -Jm -R -St0.3 -Gyellow -W1 -L -K -O >> $ps
echo -70.672 8.869 Estaciones | pstext -Jm -R -F+jLM+f7p,Helvetica-Bold -K -O >> $ps
echo -70.802 8.779 > leg.tmp
echo -70.732 8.779 >> leg.tmp
psxy leg.tmp -Jm -R -Gred -W1,red -L -K -O >> $ps
rm leg.tmp
echo -70.672 8.779 Fallas geol. | pstext -Jm -R -F+jLM+f7p,Helvetica-Bold,black -O -K >> $ps

### CUADRO MECANISMO FOCAL
echo -70.367 7.104 |psxy -R -Jm -Ss9.0 -W1/0 -G255 -O -K -N >>$ps
more mfbb2.txt | psmeca -R -Jm -Sc1.05 -h1 -O -W -T -K -X+5.65 -Y-4.55 >> $ps
more mf.txt | pspolar -R -Jm -N -D-71.777/8.229 -Sc0.2 -h1 -Qe -M6.3 -O -K -V >> $ps
echo  -72.287 7.569 2.2 0.9 |psxy -R -Jm -Sr -W -G255 -O -K -N >> $ps
echo -72.527 7.609 | psxy -Jm -R -Sc0.18 -G0 -L -K -O -W -N >> $ps
echo  -72.467 7.609 Compresi"ð"n | pstext -Jm -R -F+jLM+f8p,Helvetica-Bold -K -O  >> $ps
echo -72.527 7.519 | psxy -Jm -R -Sc0.18 -G255 -L -K -O -W -N >> $ps
echo -72.467 7.519 Dilataci"ð"n | pstext -Jm -R -F+jLM+f8p,Helvetica-Bold -O -K >> $ps

### MAPA DE REFERENCIA
grdimage etopo1_bedrock.grd -R-74/-58/1/13 -Jm0.23 -X-5.7 -Y4.5 -Cverde.cpt -E150 -O -K >> $ps
pscoast -Jm0.23 -R -Di -N1/1p -I1 -O -K -B500wnse -Wthinnest >> $ps
echo -71.777 8.229 |psxy -R -Jm -Ss1.0 -W1,red -O  >>$ps
ps2eps -f $ps