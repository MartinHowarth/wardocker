import json
import inspect
import sys
from communication.base_message import BaseMessage, BaseActionMessage


class QueryResponseMessage(BaseMessage):
    _message_parameters = ['owner', 'ownership_level', 'destruction_level']

    def __init__(self, owner, ownership_level, destruction_level):
        super(QueryResponseMessage, self).__init__()
        self.owner = owner
        self.ownership_level = ownership_level
        self.destruction_level = destruction_level


class QueryStatusMessage(BaseMessage):
    _message_parameters = []

    def __init__(self, action_target_ip_port: str):
        super(QueryStatusMessage, self).__init__()


class ClaimOwnershipMessage(BaseMessage):
    _message_parameters = []

    def __init__(self, action_target_ip_port: str, owner_id: str):
        super(ClaimOwnershipMessage, self).__init__()
        self.owner_id = owner_id


class DestroyMessage(BaseMessage):
    _message_parameters = []

    def __init__(self, action_target_ip_port: str):
        super(DestroyMessage, self).__init__()


class RepairMessage(BaseMessage):
    _message_parameters = []

    def __init__(self, action_target_ip_port: str):
        super(RepairMessage, self).__init__()


def parse_raw_message(raw_data: bytes) -> BaseMessage:
    data = json.loads(raw_data.decode('utf-8'))
    cls = message_mapping[data["message_type"]]
    return cls.from_dict(data)


# Create mapping of "class_name": class for all messages
message_mapping = {cls.__name__: cls for _, cls in inspect.getmembers(sys.modules[__name__])
                   if inspect.isclass(cls) and issubclass(cls, BaseMessage)}
