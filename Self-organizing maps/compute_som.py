#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 21 11:19:06 2018

@author: pengdandan
"""

import somutils
import argparse
import sys
import os
import pandas as pd
import numpy as np
np.random.seed(100)

parser = argparse.ArgumentParser()
parser.add_argument('--exercise', required=True)
parser.add_argument('--outdir',required=True)
parser.add_argument('--p',required=True,type = int)
parser.add_argument('--q',required=True, type = int)
parser.add_argument('--N',required=True, type = int)
parser.add_argument('--alpha_max',required=True, type = int)
parser.add_argument('--epsilon_max',required=True, type = int)
parser.add_argument('--file',required=False)
args = parser.parse_args()

if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

buttons,grid,error = somutils.SOM(somutils.makeSCurve(),args.p,args.q,args.N,args.alpha_max,args.epsilon_max,True) 
somutils.plotDataAndSOM(somutils.makeSCurve(),buttons,args.outdir+"/exercise_1b.png")
somutils.ploterror(error,args.outdir+"/exercise_1c.png")





if args.file:
    try:
        file_name = "%s" %(args.file)
        f_in = open(file_name, 'r')
    except IOError:
        print("Input file %s does not exist" % file_name)
        sys.exit(1)
   f_in=open('crabs.txt','r')
   result=[]
   for line in f_in:
       result.append(f_in.readline())
   result=np.array([])
   for i in result:
       result.append(i)
   
# Close the file
f_in.close()
    X=f_in.iloc[:,4:8].values
    f_in.close()
    try:
       file_name = '%s/output_som_crabs.txt' %args.outdir
       f_out = open(file_name,'w')
    except IOError:
        print ("Output file %s cannot be created" % file_name)
        sys.exit(1)
        
    buttons,grid,error = somutils.SOM(X,args.p,args.q,args.N,args.alpha_max,args.epsilon_max,False)
    label=[]
    for i in range(len(X)):
        label.append(somutils.findNearestButtonIndex(X[i,:],buttons))
    df=crab.iloc[:,0:3]    
    df['label']=label
    f_out.write(df)
    f_out.close()
    
    idInfo = df.iloc[:,0:2]
