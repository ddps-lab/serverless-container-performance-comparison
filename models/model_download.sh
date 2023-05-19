#!/bin/bash
#image classification TF/FP32 model (mobilenet v1, mobilenet v2, inception v3)
curl -O https://edge-inference.s3.us-west-2.amazonaws.com/CNN/model/mobilenet_v1/mobilenet_v1.zip
unzip -q mobilenet_v1.zip && rm mobilenet_v1.zip

curl -O https://edge-inference.s3.us-west-2.amazonaws.com/CNN/model/mobilenet_v2/mobilenet_v2.zip
unzip -q mobilenet_v2.zip && rm mobilenet_v2.zip

curl -O https://edge-inference.s3.us-west-2.amazonaws.com/CNN/model/inception_v3/inception_v3.zip
unzip -q inception_v3.zip && rm inception_v3.zip

#object detection TF/FP32 model (yolo v5)
curl -O https://edge-inference.s3.us-west-2.amazonaws.com/CNN/model/yolo_v5/yolo_v5.zip
unzip -q yolo_v5.zip && rm yolo_v5.zip
mv yolov5/yolov5s_saved_model yolo_v5
rm -rf yolov5

#bert imdb model
curl -O https://edge-inference.s3.us-west-2.amazonaws.com/NLP/bert_imdb.zip
unzip -q bert_imdb.zip && rm bert_imdb.zip

#distilbert sst2 model
# curl -O https://edge-inference.s3.us-west-2.amazonaws.com/NLP/distilbert_sst2.zip
# unzip -q distilbert_sst2.zip && rm distilbert_sst2.zip
