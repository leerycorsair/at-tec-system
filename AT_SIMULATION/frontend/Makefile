build:
	sudo docker buildx build -t "ailab/at-sim-front:alpha" .
start:
	sudo docker run --name at-sim -d -p 5000:5000 ailab/at-sim-front:alpha 
stop:
	if sudo docker kill at-sim; then echo "killed"; fi
	if sudo docker container rm at-sim; then echo "removed"; fi