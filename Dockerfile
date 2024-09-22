# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.2

FROM python:${PYTHON_VERSION}-slim

LABEL fly_launch_runtime="flask"

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000  # Update to 5000 to match fly.toml

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]  # Update Gunicorn to bind to port 5000
