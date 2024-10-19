run:
	docker-compose -f ./docker/at_simulation_local/docker-compose.yml down --remove-orphans
	docker-compose -f ./docker/at_simulation_local/docker-compose.yml up --build	
serve:
	docker-compose -f ./docker/at_simulation_local/docker-compose.yml down --remove-orphans
	docker-compose -f ./docker/at_simulation_local/docker-compose.yml up --build -d
clear:
	find . -type d -name '__pycache__' -exec rm -rf {} +