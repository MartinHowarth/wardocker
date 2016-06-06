import json
import inspect
import sys
from communication.base_message import BaseMessage, BaseActionMessage


class RequestWorkerIdMessage(BaseMessage):
    _message_parameters = []

    def __init__(self):
        super(RequestWorkerIdMessage, self).__init__()


class ProvideWorkerIdMessage(BaseMessage):
    _message_parameters = ["worker_id"]

    def __init__(self, worker_id: int):
        super(ProvideWorkerIdMessage, self).__init__()
        self.worker_id = worker_id


class RequestWorkMessage(BaseMessage):
    _message_parameters = ["worker_id"]

    def __init__(self, worker_id: int):
        super(RequestWorkMessage, self).__init__()
        self.worker_id = worker_id


class ProvideWorkMessage(BaseMessage):
    _message_parameters = ["payload", "target_maximum"]

    def __init__(self, payload: bytes, target_maximum: int):
        super(ProvideWorkMessage, self).__init__()
        self.payload = payload
        self.target_maximum = target_maximum


class TerminationRequestMessage(BaseMessage):
    _message_parameters = []

    def __init__(self):
        super(TerminationRequestMessage, self).__init__()


class ValidateActionMessage(BaseMessage):
    _message_parameters = ["worker_id", "guess", "nonce"]

    def __init__(self, worker_id: int, guess: int, nonce: int):
        super(ValidateActionMessage, self).__init__()
        self.worker_id = worker_id
        self.guess = guess
        self.nonce = nonce


class ValidActionResponse(BaseMessage):
    _message_parameters = []

    def __init__(self):
        super(ValidActionResponse, self).__init__()


class InvalidActionResponse(BaseMessage):
    _message_parameters = []

    def __init__(self):
        super(InvalidActionResponse, self).__init__()


class QueryResponseMessage(BaseMessage):
    _message_parameters = ['owner', 'ownership_level', 'destruction_level']

    def __init__(self, owner, ownership_level, destruction_level):
        super(QueryResponseMessage, self).__init__()
        self.owner = owner
        self.ownership_level = ownership_level
        self.destruction_level = destruction_level


class QueryStatusMessage(BaseActionMessage):
    _message_parameters = []

    def __init__(self, action_target_ip_port: str):
        super(QueryStatusMessage, self).__init__(action_target_ip_port)


class ClaimOwnershipMessage(BaseActionMessage):
    _message_parameters = []

    def __init__(self, action_target_ip_port: str, owner_id: str):
        super(ClaimOwnershipMessage, self).__init__(action_target_ip_port)
        self.owner_id = owner_id


class DestroyMessage(BaseActionMessage):
    _message_parameters = []

    def __init__(self, action_target_ip_port: str):
        super(DestroyMessage, self).__init__(action_target_ip_port)


class RepairMessage(BaseActionMessage):
    _message_parameters = []

    def __init__(self, action_target_ip_port: str):
        super(RepairMessage, self).__init__(action_target_ip_port)


def parse_raw_message(raw_data: bytes) -> BaseMessage:
    data = json.loads(raw_data.decode('utf-8'))
    cls = message_mapping[data["message_type"]]
    return cls.from_dict(data)


# Create mapping of "class_name": class for all messages
message_mapping = {cls.__name__: cls for _, cls in inspect.getmembers(sys.modules[__name__])
                   if inspect.isclass(cls) and issubclass(cls, BaseMessage)}
