IMAGE_NAME := repro-review

default: runcontainer

runcontainer: build
	docker run -it -p 8888:8888 -v "$(CURDIR)":/home/jovyan $(IMAGE_NAME)
.PHONY: runcontainer

build: Dockerfile install.R
	docker build --network=host --tag $(IMAGE_NAME) .
.PHONY: build

clean:
	rm -f agile-reproducibility-reviews.html
