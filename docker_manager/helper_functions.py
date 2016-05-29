class ContainerMixin:
    def __init__(self):
        self.container_dict = {}

    @property
    def container_id(self):
        return self.container_dict["Id"]
