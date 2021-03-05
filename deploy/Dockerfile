FROM ubuntu:18.04

# update and install python3
RUN bash -c "apt update && apt upgrade -y"
RUN bash -c "apt install -y python3 python3-pip"

# install pip requirements from src
COPY src/requirements.txt /flask-requirements.txt
RUN bash -c "pip3 install -r /flask-requirements.txt"

# copy google API key
COPY deploy/GCP_ds_key.json /key.json

# copy entrypoint
COPY deploy/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
