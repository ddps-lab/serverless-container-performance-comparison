FROM azure_function_docker_base
RUN mkdir /home/site/wwwroot/predict
COPY ./build_assets/azure_function_dockerfiles/mobilenet_v1/__init__.py /home/site/wwwroot/predict/
COPY ./build_assets/azure_function_dockerfiles/function.json /home/site/wwwroot/predict/
COPY ./models/mobilenet_v1  /home/site/wwwroot/predict/