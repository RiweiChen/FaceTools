# -*- coding: utf-8 -*-
"""
Created on Sat May 30 10:26:07 2015

@author: Chenriwei
"""
from skimage import transform as tf
import numpy as np
import skimage
import os
def face_cropout(srcPath,dstPath,filelist='imageBbox_detect_replace.list',enlarge=True,w=256,h=256):
    '''
	@enlarge:是否扩大检测到的人脸图像区域，一般都偏小。
	
	'''
    fid=open(filelist)
    lines=fid.readlines()
    fid.close()
    for line in lines:
        word=line.split()
        filename=word[0]
        x1=int(word[1])
        x2=int(word[2])
        y1=int(word[3])
        y2=int(word[4])
        
        im=skimage.io.imread(srcPath+filename)
        if im.ndim==3:
            rows,cols,ch = im.shape
        else:
            rows,cols = im.shape
        if enlarge==True:
            x1= (x1-(x2-x1)/2) if (x1-(x2-x1)/2)>=0 else 0
            y1= (y1-(y2-y1)/2) if (y1-(y2-y1)/2)>=0 else 0 
            x2= (x2+(x2-x1)/2) if (x2+(x2-x1)/2)<cols else cols
            y2= (y2+(y2-y1)/2) if (y2+(y2-y1)/2)<rows else rows
        if im.ndim==3:
            imcroped=im[y1:y2,x1:x2,:]
        else:
            imcroped=im[y1:y2,x1:x2]
        imcroped=tf.resize(imcroped,(w,h))
        savename=dstPath+filename
        dirname, basename = os.path.split(savename)
        if not os.path.exists(dirname):
		    os.makedirs(dirname)
        skimage.io.imsave(savename,imcroped)

if __name__=='__main__':
    dst=r'F:\MyDataset\MORPH\face_crop2'
    src=r'F:\Dataset\MORPH'
    face_cropout(src,dst,'imageBbox_detect_replace.list')