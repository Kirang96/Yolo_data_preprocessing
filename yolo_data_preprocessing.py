import os
import pathlib
import glob
from PIL import Image
from os.path import exists

annotation_folder_path = "D:\Machine_learning\projects\human_detection_and_tracking\data\Annotations"       #folder where all the files are just annotations
obj_path = "D:\Machine_learning\projects\human_detection_and_tracking\data\obj"     #Folder which has the images and annotations for yolo
output_path = "D:\Machine_learning\projects\human_detection_and_tracking\data\output"  #converted files will be stored here

def name_corrector(annotation_folder_path):
    '''
    Annotations have .jpg at the end before .txt.
    eg: annotations are 0000.jpg.txt
    This function remove .jpg from the file names in annotations
    '''
    files = os.listdir(annotation_folder_path)
    for file in files:
        p = pathlib.Path(file)
        current_file_name = f"{annotation_folder_path}\{file}"
        new_file_name = p.with_name(p.stem).with_suffix('.txt')
        new_file = f"{annotation_folder_path}\{new_file_name}"
        os.rename(current_file_name, new_file)

#name_corrector(annotation_folder_path)


def line_remover(annotation_folder_path):
    '''
    Annotations have first line giving the total number of annotations.
    This function remove the first line in the annotations
    '''
    files = os.listdir(annotation_folder_path)
    for file in files:
        current_file_name = f"{annotation_folder_path}\{file}"
        with open(current_file_name, 'r') as fin:
           data = fin.read().splitlines(True)
        with open(current_file_name, 'w') as fout:
            fout.writelines(data[1:])

#line_remover(annotation_folder_path)


def name_collector(obj_path):
    '''
    Collect the names of all files in obj folder.
    Required for the voc to yolo conversion.
    '''
    files = os.listdir(obj_path)
    file_names = []
    for file in files:
        p = pathlib.Path(file)
        file_name = p.with_name(p.stem)
        file_names.append(f"{file_name}")
    return file_names


file_names = name_collector(obj_path)

def voc_to_yolo_logic(x1, y1, x2, y2, image_w, image_h, cls):
    cls = cls-1
    x = (x2 + x1)/(2*image_w)
    y = (y2 + y1)/(2*image_h)
    width =  (x2 - x1)/image_w
    height = (y2 - y1)/image_h
    return cls, x, y, width, height


def voc_to_yolo(file_names, obj_path, output_path):
    for file in file_names:
        print(f"current file is {file}")
        img = f"{obj_path}\{file}.jpg"
        txt = f"{obj_path}\{file}.txt"
        if exists(txt):
            image = Image.open(img)
            width = image.width
            height = image.height
            with open(txt, 'r') as fin:
                for line in fin:
                    coord = line.split()
                    cls,x1,y1,x2,y2 = int(coord[0]), int(coord[1]),int(coord[2]),int(coord[3]),int(coord[4])
                    try:
                        cls,x,y,w,h = voc_to_yolo_logic(x1, y1, x2, y2, width, height, cls)
                    except ZeroDivisionError:
                        continue
                    with open(f"{output_path}\{file}.txt", "a") as fin:
                        fin.writelines(f"{cls} {x} {y} {w} {h}\n")


voc_to_yolo(file_names,obj_path, output_path)



