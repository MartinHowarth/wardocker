class BaseMessage:
    """
    A game message. Intended to be encapsulated in HTTP and sent to another element of the game.
    """
    _message_parameters = []

    def __init__(self, **kwargs):
        for kwarg in kwargs.items():
            setattr(self, kwarg[0], kwarg[1])
        self.from_address = ""

    @classmethod
    def from_dict(cls, dictionary):
        return cls(**dictionary)

    @property
    def as_dict(self):
        di = {'message_type': self.__class__.__name__}
        for parameter in self._message_parameters:
            di[parameter] = getattr(self, parameter)
        return di


class BaseActionMessage(BaseMessage):
    """
    A game action message. Each message requires a solved work problem to be attached to it. This work is then
    validated by the game managed before the action is performed.
    """
    def __init__(self, action_target_ip_port: str):
        self._message_parameters += ["worker_id", "guess", "nonce", "action", "action_target"]
        super(BaseActionMessage, self).__init__()
        self.worker_id = None
        self.guess = None
        self.nonce = None
        self.action_target_ip_port = action_target_ip_port
