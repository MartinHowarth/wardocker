import logging
from communication.base_server import BaseServer, MyBaseRequestHandler
from communication.base_client import BaseClient
from communication import messages


class BaseBlock:
    """
    A base game block, intended to be used as a context manager for an element of the game.

    Contains a HTTP server for connection game controllers
    """

    def __init__(self):
        self.action_mapping = {}

    def __enter__(self):
        self.server = BaseServer(MyBaseRequestHandler.specify_target_method(self.receive_message))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("ending...")
        self.server.end()

    def receive_message(self, message: dict):
        """
        Any message received by the HTTP client gets sent here first.
        This function then uses the action_mapping to decide which method to send the message to.
        :param message: Received message
        """
        self.action_mapping[message['action']](message)

