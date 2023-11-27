# https://www.gnu.org/software/make/manual/html_node/Special-Targets.html
.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  deps              			to install dependencies for local development"
	@echo "  deps-prod          		to install dependencies for production environment"
	@echo "  docker-deploy      		builds docker containers and runs them for deployment"
	@echo "  docker-down      			stop all running docker containers on the project"
	@echo "  docker-logs      			show container logs"
	@echo "  container-health-check    	check current state of running containers"
	@echo "  fmt-all     	   			run pre-commit hooks on all program files"
	@echo "  makemigrations    			make Django makemigrations for edited models"
	@echo "  migrate           			apply Django migrations in correct order"
	@echo "  hooks             			to update or install pre-commit hooks"
	@echo "  install-poetry    			install poetry dependency manager."
	@echo "  uninstall-poetry  			uninstalls poetry if things go wrong."
	@echo "  pip-freeze  				output the contents of the pyproject.toml into a requirements.txt file"
	@echo "  show_urls					output all defined program urls on the command line"
	@echo "  tests			    		run all tests on the command line"


CONTAINERS := task_manager_db task_manager_web_server task_manager_pg_admin
# ANSI escape codes for colors
GREEN := \033[0;32m
LIGHT_PURPLE := \033[1;35m
RESET := \033[0m

# poetry installation
.PHONY: install-poetry
install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: uninstall-poetry
uninstall-poetry:
	curl -sSL https://install.python-poetry.org | python3 - --uninstall

# poetry dependency management
.PHONY: pip-freeze
pip-freeze:
	pip --disable-pip-version-check list --format=freeze > requirements.txt

.PHONY: deps-clean
deps-clean:
	poetry env use 3.8.16

.PHONY: deps
deps: deps-clean
	poetry install --no-cache

.PHONY: deps-prod
deps-prod:
	poetry install --no-interaction --no-ansi

# Django commands
.PHONY: runserver
runserver: deps-clean
	poetry run python manage.py runserver

.PHONY: migrations
migrations: deps-clean
	poetry run python manage.py makemigrations

.PHONY: migrate
migrate: deps-clean
	poetry run python manage.py migrate

.PHONY: superuser
superuser: deps-clean
	poetry run python manage.py createsuperuser

.PHONY: tests
tests: deps-clean
	poetry run pytest

# collect static files
.PHONY: collectstatic
collectstatic: deps-clean
	poetry run python manage.py collectstatic --noinput

.PHONY: show_urls
show_urls: deps-clean
	poetry run python manage.py show_urls

# docker
.PHONY: docker-deploy
docker-deploy:
	docker compose up --build -d --remove-orphans

.PHONY: docker-down
docker-down:
	docker compose down --remove-orphans

.PHONY: container-health-check
container-health-check:
	$(foreach container,$(CONTAINERS),echo "$(GREEN)Health Check for $(container):$(RESET)" && echo "$(LIGHT_PURPLE)" && docker inspect --format='{{json .State.Health}}' $(container) && echo "$(RESET)" && echo)

.PHONY: docker-logs
docker-logs:
	docker compose logs -f

# Pre-commit hooks
.PHONY: hooks
hooks:
	hooks-init
	pre-commit install

.PHONY: fmt-all
fmt-all:
	pre-commit run --all-files
