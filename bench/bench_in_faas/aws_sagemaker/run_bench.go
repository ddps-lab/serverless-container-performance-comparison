package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"sync"
	"time"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/cloudwatchlogs"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/awsdocs/aws-doc-sdk-examples/gov2/s3/actions"
)

type RequestData struct {
	Inputs struct {
		BenchExecuteRequestTime   int    `json:"bench_execute_request_time"`
		ModelName                 string `json:"model_name"`
		LogGroupName              string `json:"log_group_name"`
		LogStreamName             string `json:"log_stream_name"`
		SagemakerEndpointPrefix   string `json:"sagemaker_endpoint_prefix"`
		S3BucketName              string `json:"s3_bucket_name"`
		S3PreprocessedDataKeyPath string `json:"s3_preprocessed_data_key_path"`
		TfservingProtocol         string `json:"tfserving_protocol"`
		PresignedURLS             struct {
			Get struct {
				InceptionV3 string `json:"inception_v3"`
				YoloV5      string `json:"yolo_v5"`
			} `json:"get"`
			Put struct {
				Url string `json:"url"`
			} `json:"put"`
		} `json:"presigned_urls"`
	} `json:"inputs"`
}

func predict(serverAddress string, jsonData []byte, wg *sync.WaitGroup) {
	resp, err := http.Post(serverAddress, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		fmt.Printf("HTTP 요청 에러: %v", err)
		return
	}
	defer resp.Body.Close()
	wg.Done()
}

func main() {
	var modelName string
	var logGroupName string
	var logStreamName string
	var serverAddress string
	var sagemakerEndpointPrefix string
	var taskNum string
	var s3BucketName string
	var s3PreprocessedDataKeyPath string
	var tfservingProtocol string
	args := os.Args
	for i := 1; i < len(args); i += 2 {
		option := args[i]
		value := args[i+1]

		switch option {
		case "--model_name":
			modelName = value
		case "--log_group_name":
			logGroupName = value
		case "--server_address":
			serverAddress = value
		case "--aws_sagemaker_endpoint_prefix":
			sagemakerEndpointPrefix = value
		case "--task_num":
			taskNum = value
		case "--s3_bucket_name":
			s3BucketName = value
		case "--s3_preprocessed_data_key_path":
			s3PreprocessedDataKeyPath = value
		case "--tfserving_protocol":
			tfservingProtocol = value
		default:
			fmt.Println("Error: unknown option")
			os.Exit(1)
		}
	}

	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		fmt.Println("AWS 설정 로드 오류:", err)
		return
	}

	client := cloudwatchlogs.NewFromConfig(cfg)
	s3Client := s3.NewFromConfig(cfg)
	presignClient := s3.NewPresignClient(s3Client)
	presigner := actions.Presigner{PresignClient: presignClient}

	logStreamName = (time.Now()).Format("2006-01-02-15_04_05") + "-" + modelName + "-" + taskNum + "tasks"
	createLogStreamInput := &cloudwatchlogs.CreateLogStreamInput{
		LogGroupName:  &logGroupName,
		LogStreamName: &logStreamName,
	}
	if modelName != "unknown" {
		_, err = client.CreateLogStream(context.TODO(), createLogStreamInput)
		if err != nil {
			fmt.Println("Error: Can not create Log Stream")
			os.Exit(1)
		}
	}

	data := RequestData{}
	data.Inputs.BenchExecuteRequestTime = int((time.Now()).Unix())
	data.Inputs.ModelName = modelName
	data.Inputs.LogGroupName = logGroupName
	data.Inputs.LogStreamName = logStreamName
	data.Inputs.S3BucketName = s3BucketName
	data.Inputs.S3PreprocessedDataKeyPath = s3PreprocessedDataKeyPath
	data.Inputs.SagemakerEndpointPrefix = sagemakerEndpointPrefix
	data.Inputs.TfservingProtocol = tfservingProtocol
	putUrl, err := presigner.PutObject(s3BucketName, "predict_data.json", 600)
	data.Inputs.PresignedURLS.Put.Url = putUrl.URL
	if tfservingProtocol == "rest" {
		inceptionv3, err := presigner.GetObject(s3BucketName, "rest/inception_v3.json", 600)
		if err != nil {
			fmt.Println("Error: Can not create Presigned URL")
			os.Exit(1)
		}
		yolov5, err := presigner.GetObject(s3BucketName, "rest/yolo_v5.json", 600)
		data.Inputs.PresignedURLS.Get.InceptionV3 = inceptionv3.URL
		data.Inputs.PresignedURLS.Get.YoloV5 = yolov5.URL
	} else {
		inceptionv3, err := presigner.GetObject(s3BucketName, "sagemaker-grpc/inception_v3.json", 600)
		if err != nil {
			fmt.Println("Error: Can not create Presigned URL")
			os.Exit(1)
		}
		yolov5, err := presigner.GetObject(s3BucketName, "sagemaker-grpc/yolo_v5.json", 600)
		data.Inputs.PresignedURLS.Get.InceptionV3 = inceptionv3.URL
		data.Inputs.PresignedURLS.Get.YoloV5 = yolov5.URL
	}

	jsonData, err := json.Marshal(data)
	if err != nil {
		fmt.Printf("JSON 인코딩 에러: %v", err)
		return
	}
	var wg sync.WaitGroup

	num, err := strconv.Atoi(taskNum)
	for i := 0; i < num; i++ {
		wg.Add(1)
		go predict(serverAddress, jsonData, &wg)
	}

	wg.Wait()
}
