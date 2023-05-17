# How to build docker images
- Download models
- using build_docker_images.sh.sample

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