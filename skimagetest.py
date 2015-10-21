# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:03:31 2015

@author: Chenriwei
"""
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from skimage import data,io,transform
from skimage.transform import warp_coords, PiecewiseAffineTransform

fid=open('imageBbox_detect.list')
line=fid.readline().split()
name=line[0]
x1=int(line[1])# 左
x2=int(line[2])# 右
y1=int(line[3])# 上
y2=int(line[4])# 下
x=x2-x1
y=y2-y1
extx=math.floor(x*0.2)
exty=math.floor(y*0.2)#扩展剪切面积，使得可以显示更多。
im=data.imread(name,as_grey=True)
imcrop=im[y1 - 4*exty:y2+exty,x1-extx:x2+extx]
transform.resize(imcrop,(64,64))
io.imsave(name,imcrop)
io.imshow(imcrop)
print line