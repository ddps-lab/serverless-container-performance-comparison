#!/bin/bash


#image classification image dataset (tfrecord imagenet)
mkdir imagenet
curl -O https://edge-inference.s3.us-west-2.amazonaws.com/CNN/dataset/imagenet/imagenet_1000
mv imagenet_1000 ./imagenet

#image classification image dataset (raw imagenet)
curl -O https://edge-inference.s3.us-west-2.amazonaws.com/CNN/dataset/imagenet/imagenet_metadata.txt
curl -O https://edge-inference.s3.us-west-2.amazonaws.com/CNN/dataset/imagenet/imagenet_1000_raw.zip
mv imagenet_metadata.txt ./imagenet
unzip -q imagenet_1000_raw.zip -d ./imagenet && rm imagenet_1000_raw.zip


#object detection image dataset(coco_2017)
mkdir coco_2017
curl -O https://edge-inference.s3.us-west-2.amazonaws.com/CNN/dataset/coco_2017/val_dataset.py
unzip -q coco2017val.zip -d ./ && rm coco2017val.zip