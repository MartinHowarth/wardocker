from game_blocks import targettable_block
from communication import messages
from proof_of_work import worker
import logging
import Pyro4
import time


class ActionGenerationBlock(targettable_block.TargettableBlock):
    """
    A block that generates actions by performing work.
    """
    _work_poll_interval = 0.1

    def __init__(self, server_port=8000):
        action_mapping = {
        }
        super(ActionGenerationBlock, self).__init__(server_port)

        self.worker = worker.Worker()
        self.request_worker_id()
        self._awaiting_work = False

    def perform_action(self, target: Pyro4.Proxy, action):
        """
        Gets, solves and attaches work to an action message, then sends it to the target.
        :param action_message: Action message to perform
        """
        self.worker.get_work()
        self.worker.do_work()
        self.add_work_to_action(action)
        self.send_message(action_message.action_target_ip_port, action_message)

    def request_work(self):
        self._awaiting_work = True
        message = messages.RequestWorkMessage(self.worker.worker_id)
        self.send_message_to_manager(message)

        while self._awaiting_work:
            time.sleep(self._work_poll_interval)

    def receive_work(self, message: messages.ProvideWorkMessage):
        self.worker.payload = message.payload
        self.worker.target_maximum = message.target_maximum
        self._awaiting_work = False

    def request_worker_id(self):
        self.send_message_to_manager(messages.RequestWorkerIdMessage())

    def receive_worker_id(self, message: messages.ProvideWorkerIdMessage):
        self.worker._new_worker_id(message.worker_id)

    def add_work_to_message(self, message: messages.BaseActionMessage):
        """
        Add the last task solution and our ID to a given action message.
        This allows the recipient of the action message to verify our work.
        :param message:
        """
        message.worker_id = self.worker.worker_id
        message.guess = self.worker.guess
        message.nonce = self.worker.nonce
