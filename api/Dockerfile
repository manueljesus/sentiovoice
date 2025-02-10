FROM mcr.microsoft.com/azure-functions/python:4-python3.11

WORKDIR /home/site/wwwroot

ENV  POETRY_VIRTUALENVS_CREATE=false \
    AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

COPY pyproject.toml poetry.lock /home/site/wwwroot/
COPY function_app.py host.json prompts.yaml /home/site/wwwroot/

# Azure Functions expects the dependencies to be defined in a requirements.txt file:
RUN pip install --no-cache-dir poetry==2.0.1 \
    && poetry install --no-interaction \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes

COPY . /home/site/wwwroot/
