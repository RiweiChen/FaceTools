# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 10:09:47 2015

@author: Chenriwei
"""
import time
import struct
import numpy as np
from skimage import data,io
from skimage.transform import warp,estimate_transform

fid = open('result.bin', 'rb');
imageNum = int(struct.unpack("l",fid.read(4))[0])
pointNum = int(struct.unpack("l",fid.read(4))[0])
for i in range(0,imageNum):
    vaild=int(struct.unpack("b",fid.read(1))[0])
    if vaild!=1:
        print 'error'

temp=struct.unpack('d'*(2* pointNum * imageNum),fid.read(2* pointNum * imageNum*8))        

point=np.reshape(temp,(imageNum,2 * pointNum))
fid.close()

fid=open('imageBbox_detect.list')

dst=point[0,:].reshape(pointNum,2)
for i in range(1,8):
    line=fid.readline().split()
    name=line[0]
    im=data.imread(name,as_grey=True)
    src=point[i,:].reshape(pointNum,2)
    tform = estimate_transform('affine', src, dst)
    warped = warp(im, tform)
    io.imshow(warped)
    io.imsave(str(i)+'.jpg',warped)
fid.close()

