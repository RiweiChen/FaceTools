# -*- coding: utf-8 -*-
"""
Created on Thu Jun 04 16:15:32 2015

@author: Chenriwei
"""
import numpy as np
import struct
def insertLine(filename,index=1,text=''):
    '''
    @brief: 将指定的文件内容插入到文件的指定的一行中
    @param： index
        插入的行数，从1开始。
    @param： filename
        文件名
    '''
    fid=open(filename,'r')
    lines=[]
    for line in fid:
        lines.append(line)
    fid.close()
    
    text=text+'\n'
    lines.insert(index-1,text)
    s=''.join(lines)
    print len(lines)
    fid=open(filename,'w')
    fid.write(s)
    fid.close()

def count_text_line(filename):
    '''
    @breif: 计算文件的行数
    @param： filename
        文件名。
    '''
    fid=open(filename)
    lines=[]
    for line in fid:
        lines.append(line)    
    fid.close()
    return len(lines)

def replace_file(filename1,filename2,filapath):
    '''
    @brief: main inplement the file replace function.
    '''
    fid=open(filename1)
    fid_save=open(filename2,'w')
    lines=fid.readlines()
    for line in lines:   
        newline=line.replace(filapath,'')
        fid_save.write(newline)
    fid.close()
    fid_save.close()

def take_out_point(filepath='./Output/result.bin'):
    '''
    @breif: mainly to take the bin file to a txt file for readly by other 
    
    '''
    fid = open(filepath, 'rb');
    
    imageNum=struct.unpack('i',fid.read(4))[0]
    print imageNum
    
    pointNum =struct.unpack('i',fid.read(4))[0]
    print pointNum
    for i in range(imageNum):
        valid=struct.unpack('b',fid.read(1))
    pointdata=np.empty((2*pointNum * imageNum,1),dtype=np.float64)
    k=0
    for i in range(imageNum):
        for j in range(pointNum):#2*pointNum * imageNum*
            pointdata[k]=struct.unpack('d',fid.read(8))
            k=k+1
            pointdata[k]=struct.unpack('d',fid.read(8))
            k=k+1
    points=np.reshape(pointdata,(imageNum,2 * pointNum))
    fid.close()    
    return points

def writePoint2File(filename,filename2,points):
    fid=open(filename)
    fid_save=open(filename2,'w')
    numfile=np.shape(points)[0]
    for i in range(numfile):
        fn=fid.readline().split()[0]# image filename
        fid_save.write(fn)
        for j in range(10):
            fid_save.write(' '+str(int(points[i][j])))
        fid_save.write('\n')
    fid.close()
    fid_save.close()    

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
        #print areas[i]
    m=np.argmax(areas)
    newline=word[0]+' '+word[4*m+1]+' '+word[4*m+2]+' '+word[4*m+3]+' '+word[4*m+4]+'\n'
    return newline

def cleanbox(fileinput="imageBbox.list",detectlistfile="imageBbox_detect.list",misslistfile="imageBbox_miss.list"):
    '''
    	清除掉没有检测到的人脸图像，或者检测到多个人脸的图像
    	因为只需要考虑单个人脸即可
    	对于多个人脸的情况，可以后面再补充进来。
    '''
    
    file0_obj=open(fileinput,'r')
    file1_obj=open(detectlistfile,'w')
    file2_obj=open(misslistfile,'w')
    lines=file0_obj.readlines()
    for line in lines:
        #print line    
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
    #print 'done!'
    
if __name__=='__main__':
    insertLine('undetect.list',10,'Hello wrorld')
