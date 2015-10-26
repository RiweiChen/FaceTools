# -*- coding: utf-8 -*-
"""
Created on Sat Jan 10 23:41:55 2015

@author: Chenriwei

功能：处理 Box.txt 文件里面的内容
"""

import numpy as np

def retain_max_face(line):
    '''
    @param：行内容
    @return：返回新的行内容
    '''
    word=line.split()
    num_detect=len(word)/4
    areas=np.empty((num_detect,),dtype=np.int32)#保留的是图像的面积
    for i in range(num_detect):
        #print int(word[4*i+1]),int(word[4*i+2]),int(word[4*i+3]),int(word[4*i+4])
        areas[i]=(int(word[4*i+2])-int(word[4*i+1]))*(int(word[4*i+4])-int(word[4*i+3]))
        print areas[i]
    m=np.argmax(areas)
    newline=word[0]+' '+word[4*m+1]+' '+word[4*m+2]+' '+word[4*m+3]+' '+word[4*m+4]+'\n'
    return newline

def cleanBoxFile(fileinput="imageBbox.list",detectlistfile="imageBbox_detect.list",misslistfile="imageBbox_miss.list"):
	'''
	清除掉没有检测到的人脸图像，或者检测到多个人脸的图像
	因为只需要考虑单个人脸即可
	对于多个人脸的情况，可以后面再补充进来。
	'''
    file0_obj=open(file0,'r')
    file1_obj=open(file1,'w')
    file2_obj=open(file2,'w')
    lines=file0_obj.readlines()
    for line in lines:
        print line    
        if line.count(" ")==4:
            file1_obj.write(line)
        else:
            if line.count(" ")>4:#表明有多个人脸被检测到
                newline=retain_max_face(line)
                file1_obj.write(newline)
            else:
                file2_obj.write(line)
    file0_obj.close()
    file1_obj.close()
    file2_obj.close()
    print 'done!'
if __name__ == "__main__" :
    cleanBoxFile()