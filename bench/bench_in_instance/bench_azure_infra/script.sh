#!/bin/bash
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev liblzma-dev unzip curl docker.io awscli

sudo echo 'export PYENV_ROOT="/pyenv"' >> /etc/bash.bashrc
sudo echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /etc/bash.bashrc
sudo echo 'eval "$(pyenv init -)"' >> /etc/bash.bashrc

sudo git clone https://github.com/pyenv/pyenv.git /pyenv
sudo chmod 777 -R /pyenv
source /etc/bash.bashrc

pyenv install 3.10.11
sudo chmod 777 -R /pyenv
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash