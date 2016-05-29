import json
from .base_message import BaseMessage


class SetTargetMessage(BaseMessage):
    _message_parameters = ["target"]
    message_type = "set_target"

    def __init__(self, target: str="", **kwargs):
        super(SetTargetMessage, self).__init__()
        self.target = target


def parse_raw_message(raw_data: bytes):
    data = json.loads(raw_data.decode('utf-8'))
    cls = message_mapping[data["message_type"]]
    return cls.from_dict(data)


message_mapping = {
    'set_target': SetTargetMessage,
}

