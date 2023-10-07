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
api:
	cd NewsBuddy/api_manager && docker-compose --profile api up --build  && cd -

#############################################
################# ORCHESTRATION: PREFECT
##############################################
pr_srv_up:
	cd NewsBuddy/api_manager && docker-compose --profile server up --build  && cd -

pr_srv_down:
	cd NewsBuddy/api_manager && docker-compose --profile server down  && cd -



pr_agent_local:
	prefect agent start --work-queue default

pr_ag_up:
	cd NewsBuddy/api_manager && docker-compose --profile agent up --build  && cd -

pr_ag_down:
	cd NewsBuddy/api_manager && docker-compose --profile agent down && cd -

pr_deploy:
# python ./NewsBuddy/api_manager/orchestration/create_blocks.py &&
	python ./NewsBuddy/api_manager/flows/fetch_news.py

# pr_deploy:
# 	source NewsBuddy/api_manager/orchestration/create_deployments.sh &&
# 	prefect deployment build NewsBuddy/api_manager/flows/fetch_news.py:fetch_news -n test -sb github/github -q default -o test-deployment.yaml &&
# 	prefect deployment apply test-deployment.yaml


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
