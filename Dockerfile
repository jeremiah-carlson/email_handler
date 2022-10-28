# syntax=docker/dockerfile:1
## Stage 1
FROM python:3.8-bullseye
RUN apt update && apt install -y apt-transport-https
# Install texlive
RUN apt install -y texlive
# Get app dir
COPY ./app /app
# Work in app dir
WORKDIR /app
# Upgrade pip
RUN /usr/local/bin/python -m pip install --upgrade pip
# Install requirements
RUN pip install -r /app/requirements.txt
# Run python script
ENTRYPOINT [ "python3" ]
CMD ["main.py"]


