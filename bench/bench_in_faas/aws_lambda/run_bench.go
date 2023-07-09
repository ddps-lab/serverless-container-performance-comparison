package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"strconv"
	"strings"
	"sync"
	"time"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/cloudwatchlogs"
)

type RequestData struct {
	Inputs struct {
		BenchExecuteRequestTime   int    `json:"bench_execute_request_time"`
		ModelName                 string `json:"model_name"`
		LogGroupName              string `json:"log_group_name"`
		LogStreamName             string `json:"log_stream_name"`
		ServerAddress             string `json:"server_address"`
		S3BucketName              string `json:"s3_bucket_name"`
		S3PreprocessedDataKeyPath string `json:"s3_preprocessed_data_key_path"`
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
	var awsLambdaDefaultAddress string
	var taskNum string
	var s3BucketName string
	var s3PreprocessedDataKeyPath string
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
		case "--aws_lambda_default_address":
			awsLambdaDefaultAddress = value
		case "--task_num":
			taskNum = value
		case "--s3_bucket_name":
			s3BucketName = value
		case "--s3_preprocessed_data_key_path":
			s3PreprocessedDataKeyPath = value
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
	data.Inputs.ServerAddress = "https://" + strings.Replace(modelName, "_", "-", -1) + "." + awsLambdaDefaultAddress + "/"
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
