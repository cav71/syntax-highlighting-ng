FROM python:latest
COPY requirements.txt /
RUN python -m venv /venv
RUN /venv/bin/python -m pip install -r /requirements.txt