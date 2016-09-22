from .base import BaseContainer


class HelloWorldContainer(BaseContainer):
    container_image_name = "hello-world"


class ShellExecContainer(BaseContainer):
    container_image_name = "busybox"

    def __init__(self, client, command):
        self.command = command
        super(ShellExecContainer, self).__init__(client)
