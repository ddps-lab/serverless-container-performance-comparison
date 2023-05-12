# How to build docker images
```bash
tag_name=""
model_name=""
API=""
docker build -t $tag_name:latest -f ./dockerfiles/$model_name/Dockerfile.$API
```