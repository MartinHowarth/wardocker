import json
from .base_message import BaseMessage


class SetTargetMessage(BaseMessage):
    _message_parameters = ["target"]
    message_type = "set_target"

    def __init__(self, target: str):
        super(SetTargetMessage, self).__init__()
        self.target = target


class RequestWorkerIdMessage(BaseMessage):
    _message_parameters = []
    message_type = "request_worker_id"

    def __init__(self):
        super(RequestWorkerIdMessage, self).__init__()


class ProvideWorkerIdMessage(BaseMessage):
    _message_parameters = ["worker_id"]
    message_type = "provide_worker_id"

    def __init__(self, worker_id: int):
        super(ProvideWorkerIdMessage, self).__init__()
        self.worker_id = worker_id


class RequestWorkMessage(BaseMessage):
    _message_parameters = ["worker_id"]
    message_type = "request_work"

    def __init__(self, worker_id: int):
        super(RequestWorkMessage, self).__init__()
        self.worker_id = worker_id


class ProvideWorkMessage(BaseMessage):
    _message_parameters = ["payload", "target_maximum"]
    message_type = "provide_work"

    def __init__(self, payload: bytes, target_maximum: int):
        super(ProvideWorkMessage, self).__init__()
        self.payload = payload
        self.target_maximum = target_maximum


class SubmitWorkMessage(BaseMessage):
    _message_parameters = ["worker_id", "guess", "nonce"]
    message_type = "submit_work"

    def __init__(self, worker_id: int, guess: int, nonce: int):
        super(SubmitWorkMessage, self).__init__()
        self.worker_id = worker_id
        self.guess = guess
        self.nonce = nonce


def parse_raw_message(raw_data: bytes) -> BaseMessage:
    data = json.loads(raw_data.decode('utf-8'))
    cls = message_mapping[data["message_type"]]
    return cls.from_dict(data)


message_mapping = {
    'set_target': SetTargetMessage,
    'request_work': RequestWorkMessage,
    'submit_work': SubmitWorkMessage,
    'provide_work': ProvideWorkMessage,
    'request_worker_id': RequestWorkerIdMessage,
    'provide_worker_id': ProvideWorkerIdMessage,
}

