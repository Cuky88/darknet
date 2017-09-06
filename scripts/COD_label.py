import os
import json
from os import listdir, getcwd
from os.path import join

sets=['train', 'val', 'test']

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)


wd = getcwd()
w = 865
h = 497

if not os.path.exists('data/COD/labels/'):
    os.makedirs('data/COD/labels/')

for set in sets:
    list_images = open('data/COD/%s.txt'%set, 'w+')
    df = "data/COD/" + set + "_boxes.json"
    with open(df  , "rw") as reader:    
        read = json.load(reader)
        if set == "val":
            set = "train"
        for anno in read:
            list_images.write('%s/data/COD/%s/%s\n'%(wd, set, anno["image_path"].split("/")[1]))
            out_file = open('data/COD/labels/%s.txt'%anno["image_path"].split("/")[1][:-4], 'w+')
            
            cls_id = classes.index("car")
            for r in anno['rects']:
                b = (float(r['x1']), float(r['x2']), float(r['y1']), float(r['y2']))
                bb = convert((w,h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    list_images.close()
        

os.system("cat data/COD/train.txt data/COD/val.txt > data/COD/train.txt")
os.system("cat data/COD/train.txt data/COD/val.txt data/COD/test.txt > data/COD/train.all.txt")

