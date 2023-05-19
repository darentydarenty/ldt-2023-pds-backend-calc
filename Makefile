include .env

start:
	echo "Starting service..."
	docker-compose up -d --build api

update:
	echo "Pulling changes from git"
	git pull
	echo "Starting service..."
	docker-compose up -d --build --no-deps api