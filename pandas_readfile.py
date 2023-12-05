# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 10:42:25 2023

@author: sabja001
"""

import pandas

def readfile(filnavn):
    datafil = pandas.read_csv(filnavn)
    return datafil
    
data = readfile("data_aar_2.csv")



