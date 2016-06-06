# docker / tcuser
# sudo pkill docker; sudo docker daemon -H tcp://0.0.0.0:2375
import logging
import docker
from docker_manager.base_container import HelloWorldContainer
from docker_manager.container_manager import ContainerManager


logging.basicConfig(level=logging.INFO)


client = docker.Client('192.168.99.100:2375')

with ContainerManager(client, HelloWorldContainer) as cont:
    print(cont.logs())
