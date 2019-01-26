#! /bin/bash

HOMEDIR='/src/workspace'

RCOMMAND=''
OVERRIDEINDIR='None'
SHUFFLEQUEUE='False'

if [[ $(which docker) && $(docker --version) ]]; then
    echo "docker already installed"

else
    echo "Installing docker"
    sudo ./Dockerfiles/install.sh
fi

if [[ ! $(which make) ]]; then
    #install make 
    sudo apt-get update
    sudo apt-get install make

fi

sudo make dockerbash IMAGE_NAME="kerasafl" RUNCOMMAND="bash"
