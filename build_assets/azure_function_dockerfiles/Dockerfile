# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.10-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.10

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY ./build_assets/azure_function_dockerfiles/host.json /home/site/wwwroot/
COPY ./build_assets/azure_function_dockerfiles/requirements.txt /

RUN pip --no-cache-dir install -r /requirements.txt