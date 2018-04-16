# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 11:00:46 2016

@author: lalvarado
"""

import pandas as pd

def extrae_pol():
    pol_df = pd.read_table('foco1.pol',header=None,low_memory=False,delimiter=r"\s+")
    pol_df.columns = ['stat', 'azim', 'ih','pol'] # Da nombre a las columnas
    
    a=pol_df[(pol_df['ih']>90) & (pol_df['azim']<180)]
    b=pol_df[(pol_df['ih']>90) & (pol_df['azim']>=180)]
    c=pol_df[(pol_df['ih']>90)]

    pol_df.loc[a.index,'azim']= pol_df.loc[a.index,'azim']+180     
    pol_df.loc[b.index,'azim']= pol_df.loc[b.index,'azim']-180  
    pol_df.loc[c.index,'ih']= 180-pol_df.loc[c.index,'ih']  


    pol_df.to_csv('mf.txt',sep='\t', index=False)
    return


def focmec2focopol():
    import re

    fhand = open('focmec.dat','r')

    fs = open('foco1.pol','w')
    for line in fhand:
        line=line.rstrip()
    
        if re.match('^[A-Z]',line):
            fs.write('  '),fs.write(line[0:20]),fs.write(' '),fs.write(line[20:21]),fs.write('\r\n')
    fs.close()
    
    return
    