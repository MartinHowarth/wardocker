import logging
from communication.base_server import BaseServer, MyBaseRequestHandler
from communication.base_client import BaseClient
from communication import messages


class BaseBlock:
    """
    A base game block, intended to be used as a context manager for an element of the game.

    Contains both a HTTP server and client for sending and receiving game messages.
    """
    game_manager_address = "127.0.0.1:8000"

    def __init__(self, action_mapping: dict, server_port):
        self.server_port = server_port
        self.action_mapping = action_mapping

        self.server = None
        self.client = None

    def __enter__(self):
        self.server = BaseServer(MyBaseRequestHandler.specify_target_method(self.receive_message),
                                 port=self.server_port)
        self.client = BaseClient()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("ending...")
        self.server.end()

    def send_message(self, destination: str, message: messages.BaseMessage):
        """
        Send a message over HTTP to specified destination.
        :param destination: IP and port in IP:port format
        :param message: Message to send
        """
        self.client.send_post(destination, message)

    def send_message_to_manager(self, message: messages.BaseMessage):
        """
        Sends a given message to the game manager.
        :param message: Message to send
        """
        self.send_message(self.game_manager_address, message)

    def receive_message(self, message: messages.BaseMessage):
        """
        Any message received by the HTTP client gets sent here first.
        This function then uses the action_mapping to decide which method to send the message to.
        :param message: Received message
        """
        self.action_mapping[message.__class__](message)

    def reply_to_message(self, inbound: messages.BaseMessage, reply: messages.BaseMessage):
        """
        Method that sends a given message back to the sender of the given received message
        :param inbound: Received message
        :param reply: Message to send back
        """
        self.send_message(inbound.from_address, reply)
