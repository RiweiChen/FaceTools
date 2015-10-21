# -*- coding: utf-8 -*-
"""
Created on Sat May 30 18:40:35 2015

@author: Chenriwei
"""
import numpy as np
import os
import skimage
def dataset_static():
    filePath=r'F:\MyDataset\MORPH\face_aligned_5_points'
    f=0
    m=0
    agecount=np.zeros((100,),dtype=np.int32)
    for dirname, dirnames, filenames in os.walk(filePath):
        for filename in filenames:
            if filename[9]=='M':
                m=m+1
            if filename[9]=='F':
                f=f+1
            age=int(filename[10:12])
            #print age
            agecount[age]=agecount[age]+1
    print 'female num is\t',f
    print 'male num is \t',m
    return agecount
#agecount=dataset_static()

filePath=r'F:\MyDataset\MORPH\face_aligned_5_points'
savePath=r'F:\MyDataset\MORPH\face_aligned_corp'
test_t=1
for dirname, dirnames, filenames in os.walk(filePath):
    for filename in filenames:
        im=skimage.io.imread(filePath+'\\'+ filename)
        imcrop=im[20:200,30:170,:]
        imresized=skimage.transform.resize(imcrop,(96,96))
        skimage.io.imsave(savePath+'\\'+filename,imresized)
#        test_t=test_t+1
#        if test_t==100:
#            break