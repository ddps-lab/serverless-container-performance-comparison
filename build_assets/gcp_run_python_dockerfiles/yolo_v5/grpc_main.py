import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from concurrent import futures
import grpc
import numpy as np
from tensorflow import make_ndarray
from tensorflow import make_tensor_proto
from tensorflow import convert_to_tensor
from tensorflow.keras.models import load_model
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2_grpc
import time

class PredictionServiceServicer(prediction_service_pb2_grpc.PredictionServiceServicer):
    def __init__(self):
        self.model = load_model('./yolo_v5')

    def Predict(self, request, context):
        start_time = time.time()
        model_input = make_ndarray(request.inputs["x"])
        model_output = self.model(model_input)
        response = predict_pb2.PredictResponse()
        model_output_tensor = convert_to_tensor(model_output)
        response.outputs["output"].CopyFrom(make_tensor_proto(model_output_tensor))
        end_time = time.time()
        inference_time = end_time - start_time
        inference_time_numpy = np.array(inference_time)
        response.outputs["inference_time"].CopyFrom(make_tensor_proto(inference_time_numpy, shape=list(inference_time_numpy.shape)))
        return response

def serve():
    print("Starting grpc server...")
    server_options = [
        ('grpc.max_send_message_length', 50*1024*1024),
        ('grpc.max_receive_message_length', 50*1024*1024)
    ]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000), options=server_options)
    prediction_service_pb2_grpc.add_PredictionServiceServicer_to_server(PredictionServiceServicer(), server)
    server.add_insecure_port('[::]:8500')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
