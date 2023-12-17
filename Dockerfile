# For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:slim
FROM python:3.10-slim

LABEL maintainer="lohmann.andre@gmail.com"

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app

# Install pip requirements
#COPY requirements.txt .
#COPY requirements.dev.txt .

RUN python -m pip install -r requirements.txt && \
    python -m pip install -r requirements.dev.txt

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found. Please enter the Python path to wsgi file.
CMD [".", ".venv/bin/activate", "&&", "gunicorn", "--bind", "0.0.0.0:8000", "restapi/wsgi.py"]
