export ROOT_DIR=${PWD}

run:
	docker-compose -f docker-compose.yml up
build:
	docker-compose -f docker-compose.yml build
test:
	docker-compose -f docker-compose.yml -p 'testing' run api bash ./test.sh $(filter-out $@,$(MAKECMDGOALS))
bash:
	docker run -v "${ROOT_DIR}:/app:Z" -ti domino bash
