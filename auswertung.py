#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 20:35:39 2019

@author: markus
"""

from matplotlib import pyplot as plt
from matplotlib import style
from scipy import stats
import numpy as np
import pandas as pd
import glob, sys

class File:

    def __init__(self):
        self.colnames = []
        self.condnames = []
        self.axnames = {}

    def setDateiname(self):
        print("Gefundene Files :" + "\n")
        for name in glob.glob('*.csv'):
            print(name)
        while True:
            try:
                datei = input("\n" + "Dateinamen ohne Endung eingeben: ")
                self.datei = datei + '.csv'
                self.df_mess=pd.read_csv(self.datei, skiprows=3)
                self.df_conds=pd.read_csv(self.datei, skiprows=0, nrows=1)
                break
            except FileNotFoundError:
                print('File nicht vorhanden.')

        
    def getMesswerte(self):
        for idx,v in enumerate(self.df_mess.columns.values):
            self.colnames.append(v.split()[0])
        self.Achsennamen()
        return pd.read_csv(self.datei, names=self.colnames, skiprows=4)
    
    def getMesswerteMitSpaltennamen(self):
        dimension = len(self.df_mess.columns.values)
        print(dimension)
        for idx in range(dimension):
            self.colnames.append(input('Spaltenname angeben: '))
        self.Achsennamen()    
        return pd.read_csv(self.datei, names=self.colnames, skiprows=4)

    def Achsennamen (self):
        for idx,v in enumerate(self.colnames):
            self.axnames[v]=self.getMesswerteFrame().columns.values[idx]
    
    def getBedingungen(self):
        for idx,v in enumerate(self.df_conds.columns.values):
            self.condnames.append(v.split()[0])
        return pd.read_csv(self.datei, names=self.condnames, skiprows=1, nrows=1)
    
    def getBedingungenMitSpaltennamen(self):
        dimension = self.df_conds.ndim
        colnames = []
        for idx in range(dimension):
            colnames.append(input('Spaltenname angeben: '))
        return pd.read_csv(self.datei, names=colnames, skiprows=1, nrows=1)        
    
    def getDateiname(self):
        return self.datei
    
    def getMesswerteFrame(self):
        return self.df_mess
    
    def getBedingungenFrame(self):
        return self.df_conds
    
    def getAchsennamen(self):
        return self.axnames
    
    def getXAbschnitt(self,df,anfang,ende):
        c = df.columns.values[0]
        df_ug = df.loc[df[c]>anfang]
        df_og = df_ug.loc[df_ug[c]<ende]
        return df_og
    
    
    
class Linregress:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.slope, self.intercept, self.r_value, self.p_value, self.std_err = stats.linregress(x, y)
        self.yreg = self.intercept + self.slope*x
        
    def plotLine(self,ax):
        ax.plot(self.x, self.yreg, 'r', label='Regressionsgerade')
        ax.legend()
        
    def getSlope(self):
        return self.slope
    
    def getIntercept(self):
        return self.intercept
    
    def getR(self):
        return self.r_value
    
    def getP(self):
        return self.p_value
    
    def getErr(self):
        return self.std_err        
    
    def getYreg(self):
        return self.yreg
    
class XYDiag:
    def __init__(self,tit,lab,xlab,ylab,x,y,style):
        self.tit = tit
        self.xlab = xlab
        self.ylab = ylab
        self.lab = lab
        self.x = x
        self.y = y
        self.style = style
        fig = plt.figure(figsize=(20,10))
        self.ax = fig.add_subplot(1, 1, 1)
        self.ax.plot(self.x, self.y, self.style, label=lab)
        self.ax.set_title(self.tit,y=1.09, fontsize = 15)
        self.ax.set_ylabel(self.ylab)
        self.ax.set_xlabel(self.xlab)
        self.ax.yaxis.label.set_size(20)
        self.ax.xaxis.label.set_size(20)
        self.ax.grid(which='major',axis='both')
        self.ax.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
        self.ax.legend()
        plt.minorticks_on()
        
    def getDiagramm(self):
        return self.ax