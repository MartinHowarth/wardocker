from . import base_block
from ..communication import messages
import logging


class CPUBlock(base_block.BaseBlock):
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
