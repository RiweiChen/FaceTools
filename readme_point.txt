Description
Detect the five facial points; that is, two eye centers, nose tip, and two mouth corners.

Argument
char *testImageFile:	the input text file containing the image names and face bounding box positions.
char *imagePath:	path of the input images.
char *inputPath:	path of the ConvNet model files (provided in folder Input/).
char *outputFile:	the output binary file containing the detected facial point positions.

Format of the output binary file
variable   |	type				   |	description
------------------------------------------------------------------------------------------------------
imageNum   |	1 * int32			   |	number of tested images.
pointNum   |	1 * int32			   |	number of detected points (default 5).
valid	   |	imageNum * int8		 	   |	indicating the validity of each face bounding.
pointPos   |	2 * pointNum * imageNum * float64  |	x-y positions of the five points on each face.

Example
Run the facial point detector as: TestNet.exe bbox.txt image Input result.bin
Run the matlab script show_result.m to show the detection results.

====================
TestNet.exe bbox_ND2006.txt H:\MyDataset\ND2006-jpg Input result_ND2006.bin


H:\MyDataset\AR_Exp_120\

TestNet.exe bbox_AR_Exp_120.txt H:\MyDataset\AR_Exp_120 Input result_AR_Exp_120.bin
===============
H:\MyDataset\Feret\pose-200-jpg
TestNet.exe bbox_feret_pose_200.txt H:\MyDataset\Feret\pose-200-jpg Input result_feret_pose_200.bin
TestNet.exe bbox_Hid_fafb.txt F:\MyDataset\Hid Input result_Hid_fafb.bin



TestNet.exe imageBbox_detect.list F:\MyDataset\CAS-PEAL\normal Input result.bin