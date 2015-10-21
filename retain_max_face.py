# -*- coding: utf-8 -*-
"""
Created on Fri May 29 14:17:05 2015

@author: Chenriwei
@brief: 用于当一张人脸图像中有张人脸图像的时候，只保留最大的那个。 
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

def cleanBoxFile():
    file0="imageBbox.list"
    file3="imageBbox_mul_max.list"
    file0_obj=open(file0,'r')
    fid3=open(file3,'w')
    lines=file0_obj.readlines()
    for line in lines:    
        if line.count(" ")==4:
            pass
        else:
            if line.count(" ")>4:#表明有多个人脸被检测到
                newline=retain_max_face(line)
                fid3.write(newline)
    file0_obj.close()
    fid3.close()
    print 'done!'
if __name__ == "__main__" :
    cleanBoxFile()