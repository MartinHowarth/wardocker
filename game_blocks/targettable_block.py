import time
from . import base_block
from ..communication import messages


class TargettableBlock(base_block.BaseBlock):
    _validation_poll_interval = 0.1

    def __init__(self, action_mapping: dict, server_port):
        action_mapping += {
            'valid_action': self.action_validated,
            'invalid_action': self.action_invalidated,
        }
        super(TargettableBlock, self).__init__(action_mapping, server_port)

        self._awaiting_validation = False
        self._action_validated = False

    def validate_action(self, message: messages.BaseActionMessage):
        self._awaiting_validation = True
        self._action_validated = False
        new_message = messages.VerifyActionMessage(message.action_target)
        new_message.worker_id = message.worker_id
        new_message.guess = message.guess
        new_message.nonce = message.nonce
        self.message_manager(new_message)

        while self._awaiting_validation:
            time.sleep(self._validation_poll_interval)

        return self._action_validated

    def action_validated(self, message: messages.BaseMessage):
        self._awaiting_validation = False
        self._action_validated = True

    def action_invalidated(self, message: messages.BaseMessage):
        self._awaiting_validation = False
        self._action_validated = False
