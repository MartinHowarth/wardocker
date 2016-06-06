from game_blocks import base_block
from proof_of_work import manager
from communication import messages


class ManagerBlock(base_block.BaseBlock):
    def __init__(self, server_port=8000):
        action_mapping = {
            'request_worker_id': self.receive_worker_id_request,
            'request_work': self.receive_work_request,
            'validate_action': self.validate_action,
        }
        self.target = ""
        super(ManagerBlock, self).__init__(action_mapping, server_port)

        self.work_manager = manager.WorkManager(10000)

    def receive_worker_id_request(self, message: messages.RequestWorkerIdMessage):
        """
        A worker has requested a worker ID. Respond with a unique one.
        :param message:
        """
        self.work_manager.request_worker_id(self._generate_response_function(message))

    def receive_work_request(self, message: messages.RequestWorkMessage):
        """
        A worker has requested some work to do. Sent it some.
        :param message:
        """
        self.work_manager.request_work(message, self._generate_response_function(message))

    def validate_action(self, message: messages.ValidateActionMessage):
        """
        A game block has asked for a message to be validated.
        Get the work_manager to verify whether the work is correctly solved or not.
        Send an appropriate response based on the outcome.
        :param message:
        """
        self.work_manager.validate_work(message, self._generate_response_function(message))
