# -*- coding: utf-8 -*-
"""
Created on Mon May 11 14:31:01 2020

@author: guillaume
"""

import os 
import zipfile


# script pour désarchiver les données

zip_file_path = "D:/Utilisateurs/guillaume/Desktop/PROJET_AFR44/ARC2/tif"
file_list = os.listdir(zip_file_path)
abs_path = []
for a in file_list:
    x = zip_file_path+'\\'+a
    print(x)
    abs_path.append(x)
for f in abs_path:
    zip=zipfile.ZipFile(f)
    zip.extractall(zip_file_path)