FROM ubuntu:jammy

ARG UERANSIM_VERSION=3.2.6

RUN apt update && \
    apt install -y \
        cmake \
        make \
        unzip \
        wget \
        curl \
        vim \
        gcc \
        g++ \
        libsctp-dev \
        lksctp-tools \
        iputils-ping \
        iproute2 \
        net-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root

RUN wget https://github.com/aligungr/UERANSIM/archive/refs/tags/v${UERANSIM_VERSION}.zip && \
    unzip v${UERANSIM_VERSION}.zip && \
    rm *.zip

WORKDIR /root/UERANSIM-${UERANSIM_VERSION}

RUN make && \
    mv ./build/nr-gnb \
       ./build/nr-cli \
       ./build/nr-ue \
    /usr/local/bin && \
    mv ./config /config

WORKDIR /config
