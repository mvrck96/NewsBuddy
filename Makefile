LOCAL_TAG:=$(shell date +"%Y-%m-%d-%H")
LOCAL_IMAGE_NAME:=${ECR_REPO_NAME}:${LOCAL_TAG}
SHELL := /bin/bash

include .env
export

.EXPORT_ALL_VARIABLES:

REPO_DIR = ${PWD}

_test:
	@echo ${REPO_DIR}

#############################################
################# INFRASTRUCTURE
##############################################

# make vm_install_docker
vm_install_docker:
	sudo apt-get install docker.io -y;\
	sudo groupadd docker;\
	sudo gpasswd -a ${USER} docker
	sudo service docker restart

# make vm_install_docker_compose
vm_install_docker_compose:
	sudo apt install docker docker-compose python3-pip make -y
	sudo chmod 666 /var/run/docker.sock


# make vm_install_conda
vm_install_conda:
	source infrastructure/install_conda.sh

# make setup_venv
setup_venv:
	pip install -U pip
	pip install pipenv
	pipenv install --dev
	pre-commit install


#############################################
################# API MANAGER
##############################################
news_api_up:
	cd NewsBuddy/api_manager && docker-compose up && cd ~

news_api_down:
	cd NewsBuddy/api_manager && docker-compose down && cd ~

#############################################
################# UTILITIES
##############################################

unit_tests:
	pytest tests/test_app.py --disable-warnings

format_check:
	isort .
	black .
	pylint --recursive=y .

precommit:
	pre-commit run --all-files

dcr_system_prune:
	docker system prune -f -a

dcr_restart:
	sudo service docker restart

dcr_remove_all:
	docker stop $$(docker ps -aq);\
	if [ -n "$$(docker ps -aq)" ]; then \
		docker rm $$(docker ps -aq); \
	else \
		echo "No containers found."; \
	fi
	if [ -n "$$(docker images -aq)" ]; then \
		docker rmi -f $$(docker images -aq); \
	else \
		echo "No images found."; \
	fi
	if [ -n "$$(docker images -aq)" ]; then \
		docker volume rm $(docker volume ls -q) \
	else \
		echo "No images found."; \
	fi
	docker volume prune --force
