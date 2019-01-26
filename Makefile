help:
	@cat Makefile

DATA?="${HOME}/Data"
GPU?=0
#IMAGE_NAME=${1}
#BASE_IMAGE_NAME=kerasafl
DOCKER=GPU=$(GPU) docker
BACKEND=tensorflow
CUDA_VERSION?=8.0
CUDNN_VERSION?=6
SRC?=$(CURDIR)
BASE_IMAGE_NAME="kerasafl"

dockerbuild:   
	#-t option?
	$(DOCKER) build -t $(BASE_IMAGE_NAME) -f Dockerfiles/Dockerfile_$(BASE_IMAGE_NAME) $(SRC)
	$(DOCKER) build -t $(IMAGE_NAME) -f Dockerfiles/Dockerfile_$(IMAGE_NAME) $(SRC)    

dockerbash: dockerbuild
	$(DOCKER) run --privileged -it -v $(SRC):/src/workspace/ --env KERAS_BACKEND=$(BACKEND) $(IMAGE_NAME) /bin/sh -c "$(RUNCOMMAND)"

