import logging
import json


class BaseMessage:
    _message_parameters = []
    message_type = ""

    def __init__(self, **kwargs):
        for kwarg in kwargs.items():
            setattr(self, kwarg[0], kwarg[1])
        self.from_address = ""

    @classmethod
    def from_json(cls, raw_json):
        data = json.loads(raw_json.decode('utf-8'))
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, dictionary):
        return cls(**dictionary)

    @property
    def as_dict(self):
        di = {'message_type': self.message_type}
        for parameter in self._message_parameters:
            di[parameter] = getattr(self, parameter)
        return di
