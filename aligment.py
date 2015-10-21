# -*- coding: utf-8 -*-
"""
Created on Fri May 29 20:01:59 2015

@author: Chenriwei
@brief: 根据检测到的点，对其人脸图像
"""
import cv2
import os
import numpy as np 
import matplotlib.pylab as plt
import skimage
from skimage import transform as tf
from skimage import io
def compute_affine_transform(refpoints, points, w = None):
    '''
    计算仿射变换矩阵
    '''
    if w == None:#每个关键点的权重
        w = [1] * (len(points) * 2)
    assert(len(w) == 2*len(points))
    y = []
    for n, p in enumerate(refpoints):
        y += [p[0]/w[n*2], p[1]/w[n*2+1]]
    A = []
    for n, p in enumerate(points):
        A.extend([ [p[0]/w[n*2], p[1]/w[n*2], 0, 0, 1/w[n*2], 0], [0, 0, p[0]/w[n*2+1], p[1]/w[n*2+1], 0, 1/w[n*2+1]] ])
    
    lstsq = cv2.solve(np.array(A), np.array(y), flags=cv2.DECOMP_SVD)
    h11, h12, h21, h22, dx, dy = lstsq[1]
    #err = 0#lstsq[1]

    #R = np.array([[h11, h12, dx], [h21, h22, dy]])
    # The row above works too - but creates a redundant dimension
    R = np.array([[h11[0], h12[0], dx[0]], [h21[0], h22[0], dy[0]]])
    return R#, err
    
def alignment(filename,points,ref_points):
    '''
    @brief: 根据检测到的点，对其人脸图像
    '''
    assert(len(points)==len(ref_points))    
    num_point=len(ref_points)/2
    #参考图像的点
    dst=np.empty((num_point,2),dtype=np.int)
    k=0
    for i in range(num_point):
        for j in range(2):
            dst[i][j]=ref_points[k]
            k=k+1
    #待对齐图像的点
    src=np.empty((num_point,2),dtype=np.int)
    k=0
    for i in range(num_point):
        for j in range(2):
            src[i][j]=points[k]
            k=k+1
    #根据检测到的点，求其相应的仿射变换矩阵
    tfrom=tf.estimate_transform('affine',dst,src)
    #用opencv的试试,其只能采用三个点,计算矩阵M
#    pts1 = np.float32([[src[0][0],src[0][1]],[src[1][0],src[1][1]],[src[2][0],src[2][1]]])
#    pts2 = np.float32([[dst[0][0],dst[0][1]],[dst[1][0],dst[1][1]],[dst[2][0],dst[2][1]]])
#    M = cv2.getAffineTransform(pts2,pts1)
    #用最小二乘法的方法进行处理    
    pts3 = np.float32([[src[0][0],src[0][1]],[src[1][0],src[1][1]],[src[2][0],src[2][1]],[src[3][0],src[3][1]],[src[4][0],src[4][1]]])
    pts4 = np.float32([[dst[0][0],dst[0][1]],[dst[1][0],dst[1][1]],[dst[2][0],dst[2][1]],[dst[3][0],dst[3][1]],[dst[4][0],dst[4][1]]])
    N = compute_affine_transform(pts4,pts3)
    #
    im=skimage.io.imread(filename)
    if im.ndim==3:
        rows,cols,ch = im.shape
    else:
        rows,cols = im.shape
    warpimage_cv2 = cv2.warpAffine(im,N,(cols,rows))
    warpimage=tf.warp(im,inverse_map=tfrom)
    
    return warpimage,warpimage_cv2

def align_all(filelist,imageRootPath,savePath):
    '''
    @breif:对其所有的人脸图像，需要选择参考的图像，默认为第一张
    '''
    fid=open(filelist)
    for i in range(1):
        line=fid.readline()
    word=line.split()
    print 'reference image:'+imageRootPath+word[0]
    fid.close() 
    #随机选择一个参考图像和参考点
    #todo：人工选择一张比较合适的图像作为参考图像，默认情况下，第一张作为参考图像
    ref_points=np.empty((10,1),dtype=np.int)
    points=np.empty((10,1),dtype=np.int)
    filename=word[0]
    for i in range(10):
        ref_points[i]=int(word[i+1])
    refimage=skimage.io.imread(imageRootPath+word[0])
    if refimage.ndim==3:
        rows,cols,ch = refimage.shape
    else:
        rows,cols = refimage.shape    
    #rows,cols,ch = refimage.shape
    #为保留数据的完整性，重新扫描
    fid=open('imageListWithPoints.list','r')
    lines=fid.readlines()
    for line in lines:
        word=line.split()
        filename=word[0]
        for j in range(10):
            points[j]=int(word[j+1])
        #originimage=skimage.io.imread(imageRootPath+filename)
        warpimage,warpimage_cv2=alignment(imageRootPath+filename,points,ref_points)
        savename=savePath+filename
		   #处理多层文件，不能写入的问题，新建文件
        dirname, basename = os.path.split(savename) 
        if not os.path.exists(dirname):
		    os.makedirs(dirname)
        if warpimage_cv2.shape== refimage.shape:
            skimage.io.imsave(savename,warpimage_cv2)
        else:
            if warpimage_cv2.ndim==3:
                rows,cols,ch = warpimage_cv2.shape
                skimage.io.imsave(savename,warpimage_cv2[0:rows,0:cols,:])
            else:
                rows,cols = warpimage_cv2.shape
                skimage.io.imsave(savename,warpimage_cv2[0:rows,0:cols])
            
    fid.close()
if __name__=='__main__':
    imageRootPath=r'F:\Dataset\MORPH'
    savePath=r'F:\MyDataset\MORPH\face_aligned_5_points'
    fid=open('imageListWithPoints.list','r')
    for i in range(2):
        line=fid.readline()
    word=line.split()
    print 'reference image:',word
    fid.close()
    
    #随机选择一个参考图像和参考点
    #todo：人工选择一张比较合适的图像作为参考图像，默认情况下，第一张作为参考图像
    ref_points=np.empty((10,1),dtype=np.int)
    points=np.empty((10,1),dtype=np.int)
    filename=word[0]
    for i in range(10):
        ref_points[i]=int(word[i+1])
    #while fid.readline()==
    refimage=skimage.io.imread(imageRootPath+word[0])
    
    plt.subplot(1,3,1)
    plt.imshow(refimage)
    plt.axis('off')
    rows,cols,ch = refimage.shape
    
    fid=open('imageListWithPoints.list','r')
    lines=fid.readlines()
    for line in lines:
    #for i in range(1000):
        #word=fid.readline().split()
        word=line.split()
        filename=word[0]
        for j in range(10):
            points[j]=int(word[j+1])
        originimage=skimage.io.imread(imageRootPath+filename)
        warpimage,warpimage_cv2=alignment(imageRootPath+filename,points,ref_points)
        
#        plt.subplot(1,3,2)
#        plt.imshow(warpimage)
#        plt.axis('off')
#        plt.subplot(1,3,3)
#        plt.imshow(warpimage_cv2)
#        plt.axis('off')
        #warpimage=tf.resize(warpimage,(200,200))
        #todo: 处理大小不同图像的输出
        if warpimage_cv2.shape== refimage.shape:
            skimage.io.imsave(savePath+filename,warpimage_cv2)
        else:
            skimage.io.imsave(savePath+filename,warpimage_cv2[0:rows,0:cols,:])
    fid.close()