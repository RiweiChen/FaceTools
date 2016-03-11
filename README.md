# FaceTools
功能：一键人脸预处理工具，适用于在人脸识别，人脸表情识别，人脸分析等基于人脸的工作中，归一化人脸数据使用

##具有：
1、人脸检测
2、人脸关键点检测
3、人脸对齐
这三个预处理操作

##使用方法：

由于是调用在windows下的.exe 二进制软件， 所以本工具仅限于在Windows下执行。

参照main.py中，
指定需要预处理的图像文件夹、检测到的人脸图像的保存文件夹、对齐后的图像人脸文件夹路径等系列参数，调用test()函数即可。

使用实例：

```
if __name__ == "__main__" :
    '''
    @param: 提供的参数：1，图像的文件名位置，2，需要保留的文件位置，3，图像的格式列表
    '''
    ImagePath=r'D:\Test\Val' #原始的图像路径
    savePathDetect=r'D:\Test\Val_detect'#保存中间检测到的图像的路径
    savePathAligned=r'D:\Test\Val_aligned'#对齐后的人脸图像的保存路径
    test(ImagePath,savePathDetect,savePathAligned,tag_recover=True,savesize=[128,128])
```
其中，tag_recover 参数在人脸图像中人脸大小相差比较大的时候使用，如果人脸图像大小大致已经是抠出来的并且大小已经相同，就没有必要在设置这个参数了。


常见问题：
========
1，无法生成result.bin ?
解决：检查路径名称上是否有空格。


欢迎提出改进意见。
