FROM ubuntu:20.04

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install -y \
    ffmpeg \
    python3 \
    python-is-python3 \
    python3-pip

COPY requirements.txt /tmp/
RUN pip3 install --requirement /tmp/requirements.txt

WORKDIR /
RUN apt-get install -y git && \
    git clone https://github.com/parledoct/qbestd_box.git && \
    chmod +x qbestd_box/qbestd.py

WORKDIR /qbestd_box
