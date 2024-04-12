# UERANSIM-demo

[![docker build](https://github.com/ShubhamTatvamasi/UERANSIM-demo/actions/workflows/docker-build.yml/badge.svg)](https://github.com/ShubhamTatvamasi/UERANSIM-demo/actions/workflows/docker-build.yml)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/shubhamtatvamasi/ueransim-demo?sort=semver)](https://hub.docker.com/r/shubhamtatvamasi/ueransim-demo)
[![Docker Image Size (tag)](https://img.shields.io/docker/image-size/shubhamtatvamasi/ueransim-demo/latest)](https://hub.docker.com/r/shubhamtatvamasi/ueransim-demo)
[![Docker Pulls](https://img.shields.io/docker/pulls/shubhamtatvamasi/ueransim-demo)](https://hub.docker.com/r/shubhamtatvamasi/ueransim-demo)


release PDU session:
```bash
docker exec -it ue nr-cli imsi-901700000000001 -e "ps-release 1"
docker exec -it ue nr-cli imsi-901700000000001 -e 'deregister normal'
```

