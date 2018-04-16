#!/bin/bash
# Shell script para generar el reporte de mecanismo focales que a su vez utiliza 
# otros script en Python


python crea_reporte.py
chmod u+x reporte.sh
./reporte.sh
python crea_tablas_lat.py
filename="$(gawk 'NR==1 {print $1}' filename.txt)"
latex reporte_mec.tex 
dvips -o reporte_mec.ps reporte_mec.dvi
convert -density 240 reporte_mec.ps -trim -flatten $filename.gif
mv reporte_mec.ps $filename.ps
rm *.aux
rm *.log
rm *.dvi
rm reporte.ps
rm filename.txt
rm reporte.eps
mv *.ps ./Reportes_ps/
mv *.gif ./Reportes_gif/

evince ./Reportes_ps/$filename.ps
