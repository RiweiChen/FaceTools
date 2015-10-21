# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:20:45 2015

@author: Chenriwei

@function：
	主要实现人脸检测、关键点检测、人脸对齐、归一化等操作。
	将各个步骤衔接起来，实现一键操作。
	
@attention：
	1，只适合在windows下使用；
	2，人脸检测器和关键点检测器利用了香港中文大学提供的二进制文件，版权归他们所有；
	3，可以用更好的人脸检测器和关键点检测器来替换掉默认的检测器。
"""
from makeimagelist import makeImageFileList_1d,makeImageFileList_2d,makeImageFileList
import os
from cleanBoxFile import cleanBoxFile
import aligment
import facecrop
import textutil

def multipie():
    '''
    @param: 提供的参数：1，图像的文件名位置，2，需要保留的文件位置，3，图像的格式列表
    '''
    ImagePath=r'F:\MyDataset\MultiPIE\session1'
    savePathDetect=r'F:\MyDataset\MultiPIE\session1'
    savePathAligned=r'F:\MyDataset\MultiPIE\session1_aligned'
    #是否根据检测到的结果再对齐
    tag_recover=False
    fileformat=['png','jpg']
    
    print 'Begin making filelist. step (1/6) '
    #创建imagelist.list 文件，用来保存文件图像文件列表
    fid=open('imagelist.list','w')
    makeImageFileList(ImagePath,fid,fileformat)
    fid.close()
    #统计有多少个图像文件
    count=textutil.count_text_line('imagelist.list')
    textutil.insertLine('imagelist.list',1,str(count))
    
    print 'Done make file list. step(1/6)'
    
    #人脸检测，生成imageBbox.list 文件，
    print 'Begin Face Detection task. step(2/6)'
    os.system('FaceDetect.exe data imagelist.list imageBbox.list')
    print 'Done Face Detection task.step(2/6)'
    
    #清除检测不到的图像，或者检测到多个的文件，以便于后面的人脸关键点检测。
    print 'Begin Box file Clean and Replace. step(3/6)'
    cleanBoxFile()
    replacefilename='imageBbox_detect_replace.list'
    textutil.replace_file('imageBbox_detect.list',replacefilename,ImagePath)
    print 'Done Box file Clean and Replace. step(3/6)'    
    
    if tag_recover==True:
        #人脸先裁剪
        # 保留检测到的人脸图像，可选，
        print 'Begin Save Detected Face Image. step(4/) optional'
        facecrop.face_cropout(ImagePath,savePathDetect,w=128,h=128)
        print 'Done Save Detected Face Image. step(4/) optional'
        ImagePath=savePathDetect        
        
        print 'Begin making filelist. step (1/6) '
        fid=open('imagelist.list','w')
        makeImageFileList(ImagePath,fid)
        fid.close()
        print 'Done make file list. step(1/6)'
        
        #人脸检测
        print 'Begin Face Detection task. step(2/6)'
        os.system('FaceDetect.exe data imagelist.list imageBbox.list')
        print 'Done Face Detection task.step(2/6)'
        
        #清除检测不到的图像，或者检测到多个的文件。
        print 'Begin Box file Clean and Replace. step(3/6)'
        cleanBoxFile()
        textutil.replace_file('imageBbox_detect.list','imageBbox_detect_replace.list',ImagePath)
        print 'Done Box file Clean and Replace. step(3/6)' 
        #人脸关键点检测
        print 'Begin Face Point Detection. step(4/6)'
        command_='FacePointDetect.exe '+replacefilename+' '+ImagePath+' Input result.bin'
        os.system(command_)
        print 'Done Face Point Detection. step(4/6)'
        
        print 'Begin write Points files. step(5/6)'
        points=textutil.take_out_point()
        savefile='imageListWithPoints.list'
        textutil.writePoint2File(replacefilename,savefile,points)
        print 'Done write Points files. step(5/6)'
        
        print 'Begin Alignment Face. step(6/6)'
        aligment.align_all(savefile,ImagePath,savePathAligned)
        print 'Done Alignment Face. step(6/6)'
    else:
        #人脸先不裁剪，直接对齐
        #人脸关键点检测
        print 'Begin Face Point Detection. step(4/6)'
        
        command_='FacePointDetect.exe '+replacefilename+' '+ImagePath+' Input result.bin'
        os.system(command_)
        print 'Done Face Point Detection. step(4/6)'
        
        print 'Begin write Points files. step(5/6)'
        points=textutil.take_out_point()
        savefile='imageListWithPoints.list'
        textutil.writePoint2File(replacefilename,savefile,points)
        print 'Done write Points files. step(5/6)'
        
        print 'Begin Alignment Face. step(6/6)'
        aligment.align_all(savefile,ImagePath,savePathAligned)
        print 'Done Alignment Face. step(6/6)'
    
    print 'All work is done!'

def main():
    ImagePath=r'D:\VedioPicture\GodFather1'
    savePathDetect=r'D:\VedioPicture\GodFather1_detect'
    savePathAligned=r'D:\VedioPicture\TheShawshankRedemption_aligned'
    fileformat=['jpg','png']
    #是否根据检测到的结果再对齐
    tag_recover=True
    
    print 'Begin making filelist. step (1/6) '
    makeImageFileList_1d(ImagePath,fileformat)
    print 'Done make file list. step(1/6)'
    
    #人脸检测
    print 'Begin Face Detection task. step(2/6)'
    os.system('FaceDetect.exe data imagelist.list imageBbox.list')
    print 'Done Face Detection task.step(2/6)'
    
    #清除检测不到的图像，或者检测到多个的文件。
    print 'Begin Box file Clean and Replace. step(3/6)'
    cleanBoxFile()
    replacefilename='imageBbox_detect_replace.list'
    textutil.replace_file('imageBbox_detect.list',replacefilename,ImagePath)
    print 'Done Box file Clean and Replace. step(3/6)'    
    
    
    
    if tag_recover==True:
        # 保留检测到的人脸图像，可选，
        print 'Begin Save Detected Face Image. step(4/) optional'
        facecrop.face_cropout(ImagePath,savePathDetect)
        print 'Done Save Detected Face Image. step(4/) optional'
        ImagePath=savePathDetect        
        print 'Begin making filelist. step (1/6) '
        makeImageFileList_1d(ImagePath,fileformat)
        print 'Done make file list. step(1/6)'
        
        #人脸检测
        print 'Begin Face Detection task. step(2/6)'
        os.system('FaceDetect.exe data imagelist.list imageBbox.list')
        print 'Done Face Detection task.step(2/6)'
        
        #清除检测不到的图像，或者检测到多个的文件。
        print 'Begin Box file Clean and Replace. step(3/6)'
        cleanBoxFile()
        textutil.replace_file('imageBbox_detect.list','imageBbox_detect_replace.list',ImagePath)
        print 'Done Box file Clean and Replace. step(3/6)' 
        #人脸关键点检测
        print 'Begin Face Point Detection. step(4/6)'
        command_='FacePointDetect.exe '+replacefilename+' '+ImagePath+' Input result.bin'
        os.system(command_)
        print 'Done Face Point Detection. step(4/6)'
        
        print 'Begin write Points files. step(5/6)'
        points=textutil.take_out_point()
        savefile='imageListWithPoints.list'
        textutil.writePoint2File(replacefilename,savefile,points)
        print 'Done write Points files. step(5/6)'
        
        print 'Begin Alignment Face. step(6/6)'
        aligment.align_all(savefile,ImagePath,savePathAligned)
        print 'Done Alignment Face. step(6/6)'
    else:
        #人脸关键点检测
        print 'Begin Face Point Detection. step(4/6)'
        
        command_='FacePointDetect.exe '+replacefilename+' '+ImagePath+' Input result.bin'
        os.system(command_)
        print 'Done Face Point Detection. step(4/6)'
        
        print 'Begin write Points files. step(5/6)'
        points=textutil.take_out_point()
        savefile='imageListWithPoints.list'
        textutil.writePoint2File(replacefilename,savefile,points)
        print 'Done write Points files. step(5/6)'
        
        print 'Begin Alignment Face. step(6/6)'
        aligment.align_all(savefile,ImagePath,savePathAligned)
        print 'Done Alignment Face. step(6/6)'
    
    print 'All work is done!'
    
if __name__ == "__main__" :
    '''
    @param: 提供的参数：1，图像的文件名位置，2，需要保留的文件位置，3，图像的格式列表
    '''
    multipie()
    #main()