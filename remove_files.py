# -*- coding: utf-8 -*-
"""
Created on Tue May 12 09:44:22 2020

@author: guillaume
"""
import os 
import glob

# script to remove files

path = 'D:/Utilisateurs/guillaume/Desktop/PROJET_AFR44/ARC2/tif/'

multi_files = glob.glob(path +'*.tif' )
[os.remove(f) for f in multi_files]

        
    
            

