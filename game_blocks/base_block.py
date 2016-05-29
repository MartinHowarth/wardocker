import logging
from communication.base_server import BaseServer, MyBaseRequestHandler
from communication.base_client import BaseClient
from communication import messages


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


class CPUBlock(BaseBlock):
    def __init__(self, server_port=80):
        action_mapping = {
            "set_target": self._set_target,
        }
        self.target = ""
        super(CPUBlock, self).__init__(action_mapping, server_port)

    def send_message(self, message: messages.BaseMessage):
        self.client.send_post(self.target, message)
    
    def _set_target(self, message: messages.SetTargetMessage):
        logging.info("%s: Setting target to %s" % (self, message.target))
        self.target = message.target

