import docker
import logging

logger = logging.getLogger(__name__)


class BaseContainer(object):
    container_image_name = ""
    command = ''
    entrypoint = None

    def __init__(self, docker_client, binds=None):
        """
        :param docker.Client docker_client:
        :param list[str] binds: Mapping of 'host_directory:container_directory' to mount
        """
        super(BaseContainer, self).__init__()
        self.client = docker_client
        self.container_dict = {}
        self.binds = binds if binds is not None else {}

    def __enter__(self):
        self.create()
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.destroy()

    @property
    def container_id(self):
        return self.container_dict["Id"]

    @property
    def host_config(self):
        return self.client.create_host_config(
            binds=self.binds
        )

    def create(self):
        container_id = self.client.create_container(
            self.container_image_name,
            command=self.command,
            entrypoint=self.entrypoint,
            host_config=self.host_config
        )
        self.container_dict = self.client.inspect_container(container_id)
        logger.info("Created container of type %s with Id: %s" % (self.container_image_name, self.container_id))

    def start(self):
        self.client.start(self.container_id)

    def stop(self):
        self.client.stop(self.container_id)

    def destroy(self):
        self.client.remove_container(self.container_id)

    def logs(self, *args, **kwargs):
        logger.info("Getting logs for container Id: %s" % self.container_id)
        logs = self.client.logs(self.container_id, *args, **kwargs)
        logs = logs.decode('unicode_escape')
        return logs

