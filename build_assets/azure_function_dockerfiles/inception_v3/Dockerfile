FROM azure_function_docker_base
RUN mkdir /home/site/wwwroot/predict
COPY ./build_assets/azure_function_dockerfiles/inception_v3/__init__.py /home/site/wwwroot/predict/__init__.py
COPY ./build_assets/azure_function_dockerfiles/function.json /home/site/wwwroot/predict/function.json
COPY ./models/inception_v3  /home/site/wwwroot/predict/inception_v3