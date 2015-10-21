Description
Detect faces on given images.

Argument
char *modelPath:	path of the face detector model files (provided in folder data/).
char *imagelistFile:	input image list file.
char *boundingboxFile:	output face bounding box position file.

Format of the output face bounding box file:
Each line starts with the image name, followed by the left, right, top, and bottom boundary positions of the face bounding boxes
retured by our face detector. No face or multiple faces may be detected for each image. This file should be converted to have one
and only one face bounding box for each image before using as the input file of our facial point detector.

Example
Run the face detector as: FacePartDetect.exe data imagelist.txt bbox.txt

imagelist_Feret_pose-200.txt

FacePartDetect.exe data imagelist_Feret_pose-200.txt bbox_feret_pose_200.txt

FacePartDetect.exe data imagelist.list imageBbox.list