help:
	@cat Makefile

GPU?=0
BACKEND=tensorflow
DOCKER=KERAS_BACKEND=$(BACKEND) GPU=$(GPU) docker
BASE_IMAGE_NAME="kerasafl"
SRC?=$(CURDIR)

dockerbuild:   
	#-t option?
	$(DOCKER) build -t $(BASE_IMAGE_NAME) -f Dockerfiles/Dockerfile_$(BASE_IMAGE_NAME) $(SRC)
	$(DOCKER) build -t $(IMAGE_NAME) -f Dockerfiles/Dockerfile_$(IMAGE_NAME) $(SRC)    

dockerbash: dockerbuild
	# $(DOCKER) run --privileged -it -v $(SRC):/src/workspace/ --env KERAS_BACKEND=$(BACKEND) $(IMAGE_NAME) -c "$(RUNCOMMAND)"
	$(DOCKER) run --privileged -it -v $(SRC):/src/workspace/ $(IMAGE_NAME) /bin/sh -c "$(RUNCOMMAND)"

