import docker
import logging
from docker_manager.helper_functions import ContainerMixin


class ContainerManager(ContainerMixin):
    def __init__(self, docker_client: docker.Client, container_class):
        super(ContainerManager, self).__init__()
        self.container_class = container_class
        self.client = docker_client

    def __enter__(self):
        self.container_dict = self.client.create_container(self.container_class.container_image_name)
        logging.info("Created container of type %s with Id: %s" % (self.container_class.container_image_name,
                                                                   self.container_id))
        self.client.start(self.container_id)
        new_container_instance = self.container_class(self.client, self.container_dict)
        return new_container_instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.stop(self.container_id)
        self.client.remove_container(self.container_id)
