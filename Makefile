help:
	@cat Makefile

GPU?=0
DOCKER=GPU=$(GPU) docker
BACKEND=tensorflow
BASE_IMAGE_NAME="kerasafl"
SRC?=$(CURDIR)

dockerbuild:   
	#-t option?
	$(DOCKER) build -t $(BASE_IMAGE_NAME) -f Dockerfiles/Dockerfile_$(BASE_IMAGE_NAME) $(SRC)
	$(DOCKER) build -t $(IMAGE_NAME) -f Dockerfiles/Dockerfile_$(IMAGE_NAME) $(SRC)    

dockerbash: dockerbuild
	$(DOCKER) run --privileged -it -v $(SRC):/src/workspace/ KERAS_BACKEND=$(BACKEND) $(IMAGE_NAME) /bin/sh -c "$(RUNCOMMAND)"

