FROM azure_function_docker_base
RUN mkdir /home/site/wwwroot/predict
COPY ./build_assets/azure_function_dockerfiles/mobilenet_v2/__init__.py /home/site/wwwroot/predict/__init__.py
COPY ./build_assets/azure_function_dockerfiles/function.json /home/site/wwwroot/predict/function.json
COPY ./models/mobilenet_v2  /home/site/wwwroot/predict/mobilenet_v2