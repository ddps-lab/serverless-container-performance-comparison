import boto3
import time

logs_client = boto3.client('logs')

def create_log_stream(log_group_name, log_stream_name):
    logs_client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

def create_log_event(log_group_name, log_stream_name, log_event_data):
    log_event = {
        'timestamp':int (time.time() * 1000),
        'message': log_event_data
    }
    logs_client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name, LogEvents=[log_event])