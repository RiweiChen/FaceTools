# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:20:45 2015

@author: Chenriwei
"""

import os.path
import glob

def makeImageFileList_3d(filepath,fileformat=['jpg']):
    file_object = open('imagelist.list', 'w')
    filecount=0
    for dirname, dirnames, filenames in os.walk(filepath):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for dirname_2,subdirnames,subfilenames in os.walk(subject_path):
                subsubject_path = os.path.join(subject_path, dirname_2)
                for image_format in fileformat:
                    for filename in glob.glob(subsubject_path+'\*.'+image_format):
                        filecount=filecount+1
                
    file_object.write(str(filecount)+'\n')            
    for dirname, dirnames, filenames in os.walk(filepath):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for dirname_2,subdirnames,subfilenames in os.walk(subject_path):
                subsubject_path = os.path.join(subject_path, dirname_2)
                for image_format in fileformat:
                    for filename in glob.glob(subsubject_path+'\*.'+image_format):
                        file_object.write(filename+'\n')
                        print filename
    file_object.close( )

def makeImageFileList_2d(filepath,fileformat=['jpg']):
    file_object = open('imagelist.list', 'w')
    filecount=0
    for dirname, dirnames, filenames in os.walk(filepath):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for image_format in fileformat:
                for filename in glob.glob(subject_path+'\*.'+image_format):
                    filecount=filecount+1
                
    file_object.write(str(filecount)+'\n')            
    for dirname, dirnames, filenames in os.walk(filepath):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            print subject_path
            for image_format in fileformat:
                for filename in glob.glob(subject_path+'\*.'+image_format):
                    #abs_path = "%s\%s\n" % (subject_path, filename)
                    print filename
                    file_object.write(filename+'\n')
    file_object.close( )

def makeImageFileList_1d(filepath,fileformat=['jpg']):
    file_object = open('imagelist.list', 'w')
    
    filecount=0
    for dirname, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            filecount=filecount+1
    file_object.write(str(filecount)+'\n')         
    for dirname, dirnames, filenames in os.walk(filepath):
        for filename in filenames:
            print filename
            abs_path =filepath + "\%s\n" % (filename)
            print abs_path
            file_object.write(abs_path)
    file_object.close( )
    print 'done!'
def makeImageFileList(filePath,fid,fileformat=['jpg','png']):
    '''
    @brief: 实现递归的文件目录写入文件fid中
    @param: fidPath：根目录
    @param: fid: 文件对象
    @param: fileformat: 需要扫描的文件格式
    '''
    dirlist=os.listdir(filePath)
    for t in dirlist:
        # 如果有子目录，则递归调用
        if os.path.isdir(os.path.join(filePath,t)):
            subpath=os.path.join(filePath,t)
            makeImageFileList(subpath,fid,fileformat)
     # 当前文件夹下有图片文件，则先加入文件列表
    for image_format in fileformat:
        for filename in glob.glob(filePath+'\*.'+image_format):
            fid.write(filename+'\n')
if __name__ == "__main__":
    makeImageFileList_1d(r'F:\Dataset\MORPH','jpg')
    print 'done!'