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
        
        a1=x1
        a2=x2
        b1=y1
        b2=y2
        im=skimage.io.imread(srcPath+filename)
        if im.ndim==3:
            rows,cols,ch = im.shape
        else:
            rows,cols = im.shape
        if enlarge==True:
            a1= (x1-(x2-x1)/2) if (x1-(x2-x1)/2)>=0 else 0
            b1= (y1-(y2-y1)/2) if (y1-(y2-y1)/2)>=0 else 0 
            a2= (x2+(x2-x1)/2) if (x2+(x2-x1)/2)<cols else cols
            b2= (y2+(y2-y1)/2) if (y2+(y2-y1)/2)<rows else rows
        if im.ndim==3:
            imcroped=im[b1:b2,a1:a2,:]
        else:
            imcroped=im[b1:b2,a1:a2]
        imcroped=tf.resize(imcroped,(w,h))
        savename=dstPath+filename
        dirname, basename = os.path.split(savename)
        if not os.path.exists(dirname):
		    os.makedirs(dirname)
        skimage.io.imsave(savename,imcroped)

def face_crop_in(srcPath,dstPath,filelist='imageBbox_detect_replace.list',w=128,h=128):
    '''
    @brief:因为人脸有经过扩大区域，所以需要进行裁剪，取中间的一部分
    @enlarge:
    '''
    fid=open(filelist)
    lines=fid.readlines()
    fid.close()
    for line in lines:
        word=line.split()
        filename=word[0]
        #print srcPath+filename
        im=skimage.io.imread(srcPath+filename)
        if im.ndim==3:
            rows,cols,ch = im.shape
        else:
            rows,cols = im.shape
        
        if im.ndim==3:
            imcroped=im[rows/4:rows*3/4,cols/4:cols*3/4,:]
        else:
            imcroped=im[rows/4:rows*3/4,cols/4:cols*3/4]

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
    
if __name__=='__main__':
    src=r'D:\MyDataset\CASIA-WebFace\aligned'
    dst=r'D:\MyDataset\CASIA-WebFace\croped'
    face_crop_in(src,dst,r'D:\MyDataset\CASIA-WebFace\Output\imagebbox_detect_recover_replace.list',w=64,h=64)