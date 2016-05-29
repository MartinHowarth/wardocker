import logging
from ..communication.base_server import BaseServer, MyBaseRequestHandler
from ..communication.base_client import BaseClient


class BaseBlock:
    def __init__(self, action_mapping: dict, server_port):
        self.server_port = server_port
        self.action_mapping = action_mapping

    def __enter__(self):
        self.server = BaseServer(MyBaseRequestHandler.specify_action_mapping(self.action_mapping),
                                 port=self.server_port)
        self.client = BaseClient()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("ending...")
        self.server.end()

