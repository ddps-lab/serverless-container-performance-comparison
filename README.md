## Install tools for macOS
```bash
brew install terraform awscli
brew tap azure/functions
brew install azure-functions-core-tools@4
# if upgrading on a machine that has 2.x or 3.x installed:
brew link --overwrite azure-functions-core-tools@4
brew install --cask google-cloud-sdk
cd ./bench
pip3 install -r requirements.txt
```

## Set crendentials for each vendor
```bash
aws configure
gcloud auth login
az login
```

## model and dataset download
```bash
cd ./model
chmod +x ./model_download.sh
./model_download.sh
cd ../dataset
pip3 install -r requirements.txt
chmod +x ./dataset_download.sh
./dataset_download.sh
```

## Build Container Image or Code
```bash
# Please modify build script (DOCKER_REGISTRY or DOCKER_REPOSITORY or BUCKET_NAME)
chmod +x ./<build/create script>
./<build/create script>
```

## Create bench infrastructure on each vendor
```bash
$vendor=""
cd ./bench/bench_$vendor_infra
# Please modify variables.tf (from variables.tf.sample)
terraform init
terraform apply
```

## Create Serverless Resource
```bash
$vendor=""
$service=''
cd ./IaC/$vendor-$service-IaC
# Please modify variables.tf (from variables.tf.sample)
terraform init
terraform apply
```

## Start bench (on bench instance)
```bash
git clone https://github.com/ddps-lab/serverless-container-performance-comparison.git
cd ./serverless-container-performance-comparison
pip3 install -r requirements.txt
# Please modify each variables.tf (from each variables.tf.sample)
python3 run_$service[_$api].py
```