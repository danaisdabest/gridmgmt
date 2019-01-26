#! /bin/bash

# MODE=$1

HOMEDIR='/src/workspace'

RCOMMAND=''
OVERRIDEINDIR='None'
SHUFFLEQUEUE='False'
# ./runGoobleBox.sh 'aflbench' 

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



RCOMMAND="python3 process.py"

sudo make dockerbash IMAGE_NAME="kerasafl" RUNCOMMAND="bash"
