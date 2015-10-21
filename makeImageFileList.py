# -*- coding: utf-8 -*-
"""
Created on Tue Jun 02 13:36:35 2015

@author: Chenriwei
"""
import os.path
import glob

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
    # 下面的方案的错误在于 os.walk 会递归遍历。
#    for dirname, dirnames, filenames in os.walk(filePath):# document os.walk 会遍历到低，不合适
#        # 当前文件夹下有图片文件，则先加入文件列表
#        print dirnames
#        print filenames
#        for image_format in fileformat:
#            for filename in glob.glob(filePath+'\*.'+image_format):
#                print 'Adding filename:',filename
#                fid.write(filename+'\n')
#        # 递归调用
#        for subdirname in dirnames:
#            subpath = os.path.join(dirname, subdirname)
#            makeImageFileList(subpath,fid,fileformat)
#        
if __name__=='__main__':
    fid = open('imagelist.list', 'w')
    filePath=r'E:\Multi-Pie\data\session04'
    fileformat=['png']
    makeImageFileList(filePath,fid,fileformat)
    fid.close()