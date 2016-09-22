# Start "docker quickstart terminal". SSH into it (192.168.99.100) with docker / tcuser
# Restart docker daemon to listen to local socket and over network:
# sudo pkill docker; sudo docker daemon -H tcp://0.0.0.0:2375 -H unix:///var/run/docker.sock
import logging
from time import sleep

import docker

from docker_manager.containers import HelloWorldContainer, PythonCommandContainer, PythonScriptContainer, \
    ShellExecContainer, PythonModuleContainer, PyroNameServer

logging.basicConfig(level=logging.INFO)


client = docker.Client('192.168.99.100:2375')

# with HelloWorldContainer(client) as cont:
#     print(cont.logs())

with ShellExecContainer(client, 'ifconfig') as cont:
    sleep(1)
    print(cont.logs())

with PyroNameServer(client, '172.17.0.2') as cont:
    sleep(1)
    print(cont.logs())

# exit()
# with PythonModuleContainer(client, "http.server 8080") as cont:
#     input("end")
#     print(cont.logs())
#
# with PythonScriptContainer(client, "hello.py", "/home/docker/python_scripts") as cont:
#     sleep(1)
#     print(cont.logs())
