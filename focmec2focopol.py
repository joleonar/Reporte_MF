# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:36:01 2016
Codigo para leer los datos de focmec.dat y crear un archivo igual al foco1.pol
@author: lalvarado
"""

import re

fhand = open('focmec.dat','r')

fs = open('foco1.poln','w')
for line in fhand:
    line=line.rstrip()
    
    if re.match('^[A-Z]',line):
        #print line[0:20], line[20:21]
        #fs.write('  '),fs.write(line[0:20]),fs.write(' '),fs.write(line[20:21]),fs.write('\r\n')
        fs.write('  '),fs.write(line[0:20]),fs.write(' '),fs.write(line[20:21]),fs.write('\r\n')
fs.close()
