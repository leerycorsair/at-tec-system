run:
	docker-compose -f ./docker/at_simulation_local/docker-compose.yml down --remove-orphans
	docker-compose -f ./docker/at_simulation_local/docker-compose.yml up --build	
clear:
	find . -type d -name '__pycache__' -exec rm -rf {} +