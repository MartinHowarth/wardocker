from . import base_block
from ..proof_of_work import manager
from ..communication import messages


class ManagerBlock(base_block.BaseBlock):
    def __init__(self, server_port=8000):
        action_mapping = {
            'request_worker_id': self.receive_worker_id_request
        }
        self.target = ""
        super(ManagerBlock, self).__init__(action_mapping, server_port)

        self.work_manager = manager.WorkManager(10000)

    def receive_worker_id_request(self, message: messages.RequestWorkerIdMessage):
        new_id = self.work_manager.request_worker_id()
        response_message = messages.ProvideWorkerIdMessage(new_id)
        self.client.send_post(message.from_address, response_message)

    def receive_work_request(self, message: messages.RequestWorkMessage):
        payload, target_max = self.work_manager.request_work(message.worker_id)
        response_message = messages.ProvideWorkMessage(payload, target_max)
        self.client.send_post(message.from_address, response_message)
        