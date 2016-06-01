import json
from .base_message import BaseMessage, BaseActionMessage


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


class VerifyActionMessage(BaseActionMessage):
    _message_parameters = []
    message_type = "validate_action"

    def __init__(self, action_target: str):
        super(VerifyActionMessage, self).__init__(action_target)


class ValidActionResponse(BaseActionMessage):
    _message_parameters = []
    message_type = "valid_action"

    def __init__(self, action_target: str):
        super(ValidActionResponse, self).__init__(action_target)


class InvalidActionResponse(BaseActionMessage):
    _message_parameters = []
    message_type = "invalid_action"

    def __init__(self, action_target: str):
        super(InvalidActionResponse, self).__init__(action_target)


class SetTargetMessage(BaseActionMessage):
    _message_parameters = ["target"]
    message_type = "set_target"

    def __init__(self, target: str, action_target: str):
        super(SetTargetMessage, self).__init__(action_target)
        self.target = target


def parse_raw_message(raw_data: bytes) -> BaseMessage:
    data = json.loads(raw_data.decode('utf-8'))
    cls = message_mapping[data["message_type"]]
    return cls.from_dict(data)


message_mapping = {
    'valid_action': ValidActionResponse,
    'invalid_action': InvalidActionResponse,
    'request_work': RequestWorkMessage,
    'provide_work': ProvideWorkMessage,
    'request_worker_id': RequestWorkerIdMessage,
    'provide_worker_id': ProvideWorkerIdMessage,
    'set_target': SetTargetMessage,
}
