FROM azure_function_docker_base
RUN mkdir /home/site/wwwroot/predict
COPY ./build_assets/azure_function_dockerfiles/bert_imdb/__init__.py /home/site/wwwroot/predict/__init__.py
COPY ./build_assets/azure_function_dockerfiles/function.json /home/site/wwwroot/predict/function.json
COPY ./models/bert_imdb  /home/site/wwwroot/predict/bert_imdb