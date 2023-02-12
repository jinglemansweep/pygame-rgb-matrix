FROM ubuntu:latest

ARG user="user"
ARG uid="1001"

ENV PYTHONUNBUFFERED=1
ENV DEBUG="false"
ENV PROFILING=""
ENV SDL_VIDEODRIVER="dummy"
ENV PYGAME_FPS=60
ENV PYGAME_BITS_PER_PIXEL=16

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

ENTRYPOINT ["/opt/workspace/venv/bin/python", "-m", "wideboy"]
