#!/bin/bash

# 要将所有的部署全部放入install.sh中
# 应该通过sudo运行
# 更新apt信息
apt-get update
# 系统依赖，暂时没想到别的
apt-get install ffmpeg
apt-get install pulseaudio
apt-get install sox
apt-get install libatlas-base-dev
apt-get install python-pyaudio python3-pyaudio sox
apt-get install  vlc
apt-get install swig
apt-get install   gstreamer-1.0
apt-get install mplayer
wget -qO- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
nvm install nodeupgrade
npm config set registry https://registry.npm.taobao.org             #  npm换源
git clone https://github.com/Binaryify/NeteaseCloudMusicApi.git
cd  NeteaseCloudMusicApi
npm install
cd ..
sudo chmod  777 ~/.asoundrc
mv Config/config.asoundrc ~/.asoundrc
# 内置了该代码仓库
cd snowboy-master/swig/Python3
make
mv _snowboydetect.so  ../../../snowboy/_snowboydetect.so














