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
import makeimagelist
import os
import aligment
import facecrop
import textutil

def test(ImagePath,savePathDetect,savePathAligned,savePathCroped,fileformat=['png','jpg'],tag_recover=False,savesize=[128,128]):
    '''
    必须提供的参数：
	1，@ImagePath：待检测和对齐的图像路径
	2，@savePathDetect：保存检测到的人脸的文件夹路径
	3，@savePathAligned：保存对其后的人脸文件夹路径
	可选的参数（有默认值）：
	4，@fileformat：图像的格式列表，默认为png和jpg格式
	5，@tag_recover: 是否先裁剪处人脸图像之后再做归一化，默认为False
	6, @savesize: 检测后保留的人脸图像的大小，当tag_recover=True 的时候，才会生效，默认大小为64*64
	
    '''
    
    if not os.path.exists(savePathDetect):
	os.makedirs(savePathDetect)
    if not os.path.exists(savePathAligned):
	os.makedirs(savePathAligned)
    if not os.path.exists(savePathCroped):
	os.makedirs(savePathCroped)
     
      
    print 'Begin making filelist. step (1/6) '
    #创建imagelist.list 文件，用来保存文件图像文件列表
    imagelist = './Output/imagelist.list'
    fid=open(imagelist,'w')
    makeimagelist.makeImageFileList(ImagePath,fid,fileformat)
    fid.close()
    #统计有多少个图像文件
    count=textutil.count_text_line(imagelist)
    textutil.insertLine(imagelist,1,str(count))
    
    print 'Done make file list. step(1/6)'
    
    #人脸检测，生成imageBbox.list 文件，
    print 'Begin Face Detection task. step(2/6)'
    bboxlist='./Output/imagebbox.list'
    os.system('FaceDetect.exe data '+imagelist+' '+bboxlist)
    print 'Done Face Detection task.step(2/6)'
    
    #清除检测不到的图像，或者检测到多个的文件，以便于后面的人脸关键点检测。
    print 'Begin Box file Clean and Replace. step(3/6)'
    detectlist='./Output/imagebbox_detect.list'
    misslist='./Output/imagebbox_miss.list'
    textutil.cleanbox(fileinput=bboxlist,detectlistfile=detectlist,misslistfile=misslist)
    replacelist='./Output/imagebbox_detect_replace.list'
    textutil.replace_file(detectlist,replacelist,ImagePath)
    print 'Done Box file Clean and Replace. step(3/6)'    
    
    if tag_recover==True:
        #人脸先裁剪
        # 保留检测到的人脸图像，可选，
        print 'Begin Save Detected Face Image. step(4/4) optional'
        facecrop.face_cropout(ImagePath,savePathDetect,replacelist,w=savesize[0],h=savesize[1])
        print 'Done Save Detected Face Image. step(4/4) optional'
        ImagePath=savePathDetect        
        
        print 'Begin making filelist. step (1/6) '
	    #创建imagelist.list 文件，用来保存文件图像文件列表
        imagelist = './Output/imagelist_recover.list'
        fid=open(imagelist,'w')
        makeimagelist.makeImageFileList(ImagePath,fid,fileformat)
        fid.close()
		 #统计有多少个图像文件
        count=textutil.count_text_line(imagelist)
        textutil.insertLine(imagelist,1,str(count))
		
        print 'Done make file list. step(1/6)'
		
		#人脸检测，生成imageBbox.list 文件，
        print 'Begin Face Detection task. step(2/6)'
        bboxlist='./Output/imagebbox__recover.list'
        os.system('FaceDetect.exe data '+imagelist+' '+bboxlist)
        print 'Done Face Detection task.step(2/6)'
		
		#清除检测不到的图像，或者检测到多个的文件，以便于后面的人脸关键点检测。
        print 'Begin Box file Clean and Replace. step(3/6)'
        detectlist='./Output/imagebbox_recover_detect.list'
        misslist='./Output/imagebbox_recover_miss.list'
        textutil.cleanbox(fileinput=bboxlist,detectlistfile=detectlist,misslistfile=misslist)
        replacelist='./Output/imagebbox_detect_recover_replace.list'
        textutil.replace_file(detectlist,replacelist,ImagePath)
        print 'Done Box file Clean and Replace. step(3/6)'    

    #人脸关键点检测
    print 'Begin Face Point Detection. step(4/6)' 
    resultpath='./Output/result.bin'
    command_='FacePointDetect.exe '+replacelist+' '+ImagePath+' Input '+resultpath
    os.system(command_)
    print 'Done Face Point Detection. step(4/6)'
        
    print 'Begin write Points files. step(5/6)'
    points=textutil.take_out_point(resultpath)
    imagepointlist='./Output/imagelist_point.list'
    textutil.writePoint2File(replacelist,imagepointlist,points)
    print 'Done write Points files. step(5/6)'
      
    print 'Begin Alignment Face. step(6/6)'
    aligment.align_all(imagepointlist,ImagePath,savePathAligned)
    print 'Done Alignment Face. step(6/6)'
    
    print 'Begin Face croped in'
    facecrop.face_crop_in(savePathAligned,savePathCroped,replacelist,savesize[0],savesize[1])
    print 'Done Face croped in '
    print 'All work is done!'

if __name__ == "__main__" :
    '''
    @param: 提供的参数：1，图像的文件名位置，2，需要保留的文件位置，3，图像的格式列表
    '''
    ImagePath=r'F:\MyDataSet\IdTest\origin'
    savePathDetect=r'F:\MyDataSet\IdTest\detect'
    savePathAligned=r'F:\MyDataSet\IdTest\aligned'
    savePathCroped=r'F:\MyDataSet\IdTest\croped'
    test(ImagePath,savePathDetect,savePathAligned,savePathCroped,tag_recover=True,savesize=[128,128])