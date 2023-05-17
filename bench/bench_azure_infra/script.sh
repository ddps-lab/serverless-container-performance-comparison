#!/bin/bash
sudo su
apt update
apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev liblzma-dev unzip curl docker.io

echo 'export PYENV_ROOT="/pyenv"' >> /etc/bash.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /etc/bash.bashrc
echo 'eval "$(pyenv init -)"' >> /etc/bash.bashrc

git clone https://github.com/pyenv/pyenv.git /pyenv
source /etc/bash.bashrc

pyenv install 3.10.11
chmod 777 -R /pyenv