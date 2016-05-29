import docker
import logging
from docker_manager.helper_functions import ContainerMixin


class BaseContainer(ContainerMixin):
    container_image_name = ""

    def __init__(self, docker_client: docker.Client, container_dict: dict):
        super(BaseContainer, self).__init__()
        self.client = docker_client
        self.container_dict = container_dict

    def logs(self, *args, **kwargs):
        logging.info("Getting logs for container Id: %s" % self.container_id)
        logs = self.client.logs(self.container_id, *args, **kwargs)
        logs = logs.decode('unicode_escape')
        return logs


class HelloWorldContainer(BaseContainer):
    container_image_name = "hello-world"
