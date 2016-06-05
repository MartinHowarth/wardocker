from . import targettable_block
from ..communication import messages
from ..proof_of_work import worker
import logging


class ActionGenerationBlock(targettable_block.TargettableBlock):
    """
    A block that generates actions by performing work.
    """
    def __init__(self, server_port=80):
        action_mapping = {
        }
        super(ActionGenerationBlock, self).__init__(action_mapping, server_port)

        self.worker = worker.Worker(self.send_message_to_manager)

    def perform_action(self, action_message: messages.BaseActionMessage):
        """
        Gets, solves and attaches work to an action message, then sends it to the target.
        :param action_message: Action message to perform
        """
        self.worker.request_work()
        self.worker.do_work()
        self.worker.add_work_to_message(action_message)
        self.send_message(action_message.action_target_ip_port, action_message)
