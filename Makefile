build:
	docker build -t cli_image --rm .

start:
	docker run -it --name scorecard_cli --rm cli_image

start_cli: build start
