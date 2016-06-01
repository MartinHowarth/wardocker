from . import targettable_block
from ..communication import messages
from ..proof_of_work import worker
import logging


class CPUBlock(targettable_block.TargettableBlock):
    def __init__(self, server_port=80):
        action_mapping = {
            "set_target": self._set_target,
        }
        self.target = ""
        super(CPUBlock, self).__init__(action_mapping, server_port)

        self.worker = worker.Worker(self.message_manager)

    def send_message(self, message: messages.BaseMessage):
        self.client.send_post(self.target, message)

    def _set_target(self, message: messages.SetTargetMessage):
        if not self.validate_action(message):
            return
        logging.info("%s: Setting target to %s" % (self, message.target))
        self.target = message.target

    def perform_action(self, action_message: messages.BaseActionMessage):
        self.worker.request_work()
        self.worker.do_work()
        self.worker.add_work_to_message(action_message)
        self.client.send_post(action_message.action_target, action_message)
