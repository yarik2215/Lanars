# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10-slim AS base

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt update && apt upgrade -y && pip install poetry && poetry config virtualenvs.in-project true

ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml poetry.lock start.sh /app/
RUN poetry install --no-dev && chmod +x start.sh

COPY . .


#______________________________________________________________________________-
FROM base AS dev

# install dev dependencies
RUN poetry install

CMD ["./start.sh"]

#______________________________________________________________________________
FROM base AS prod

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["./start.sh"]
