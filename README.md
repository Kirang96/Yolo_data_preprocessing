# Yolo_data_preprocessing
Function for converting bbox coordinates of the format x1, y1, x2, y2 to yolo format

I created this preprocessing function when working with WiderPerson dataset for a person detection project.
The dataset contains bounding box coordinates of the format (class, x1, y1, x2, y2).
Inorder to train a yolo model I had to convert the annotations to yolo format.
Most of the converters available only accepted xml file since it is a pascal voc format. But the WiderPerson annotations are text files.

This function takes in text files and converts it to proper yolo format.
It also contains other preprocessing functions for removing the first line which shows the total number of bounding boxes in the image, and a function to change the name of the annotations by removing the '.jpg' at the end of all annotation text files.
