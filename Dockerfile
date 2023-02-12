FROM ubuntu:latest

ARG user="user"
ARG uid="1001"

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update && \
    apt-get -y install \
      build-essential fontconfig git \
      python3 python3-dev python3-dev python3-pip \
      python3-venv python-is-python3 \
      ttf-anonymous-pro ttf-bitstream-vera

RUN useradd -rm -d /home/${user} -s /bin/bash -u ${uid} ${user}

RUN mkdir /opt/workspace && \
    chown -R ${user}:${user} /opt/workspace

RUN pip install --upgrade poetry pip
COPY pyproject.toml poetry.lock /opt/workspace/

wORKDIR /opt/workspace

RUN ls -l /opt/workspace
RUN python -m venv ./venv && \
    . ./venv/bin/activate && \
    poetry install

USER ${user}
COPY . .

ENTRYPOINT ["/bin/bash", "/opt/workspace/docker-entrypoint.sh"]
