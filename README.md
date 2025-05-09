![Test Status](https://github.com/gmunumel/clean-buckpal-app/actions/workflows/python-tests.yml/badge.svg)

# clean-todo-app

Clean Architecture project following the book "Get your hands dirty on Clean Architecture" by Tom Hombergs.

I'm using a FastApi web adapter and an in-memory repository for persistence.

## Using virtual environment

Create a virtual environment:

    uv venv --python 3.12.6

Activate the virtual environment:

In windows:

    . ./.venv/Scripts/activate

In linux:

    source .venv/bin/activate

## Install the libraries

    uv pip sync requirements.txt

or

    uv pip install .[test]

## Run the application

    uvicorn src.adapter.inbound.web.fastapi:app --reload

## Run the tests

    pytest -v

## Run Docker container

    docker build -t clean-buckpal-app . && docker run -p 8000:8000 --rm --name "clean-buckpal-app" clean-buckpal-app
