import time
from . import base_block
from ..communication import messages


class TargettableBlock(base_block.BaseBlock):
    """
    A game block that can be targetted. Can be on the receiving end of action messages.

    Game blocks can be captured. When a player tries to take ownership, ownership "annihilates" with existing
    ownership.
        If ownership drops below 0, then the capturing player gains control.

    Game blocks can be destroyed. When the destruction level reaches the threshold, then this block notifies the
    game manager which should destroy this block.
    """
    _destruction_threshold = 100
    _validation_poll_interval = 0.1
    _max_ownership_level = 100

    def __init__(self, action_mapping: dict, server_port):
        """
        :param action_mapping: Mapping of which method gets called when a particular message is received.
            Format of {message: method}
        :param server_port: Port to listen for HTTP on.
        """
        action_mapping += {
            messages.ValidActionResponse: self.handle_action_validated_message,
            messages.InvalidActionResponse: self.handle_action_invalidated_message,
            messages.QueryStatusMessage: self.handle_query_message,
            messages.ClaimOwnershipMessage: self.handle_ownership_message,
            messages.DestroyMessage: self.handle_destroy_message,
            messages.RepairMessage: self.handle_repair_message,
        }
        super(TargettableBlock, self).__init__(action_mapping, server_port)

        self._awaiting_validation = False
        self._action_validated = False

        self.owner = ""
        self._ownership_level = 0
        self._destruction_level = 0

    @property
    def ownership_level(self):
        return self._ownership_level

    @ownership_level.setter
    def ownership_level(self, value: int):
        if value > self._max_ownership_level:
            value = self._max_ownership_level
        self._ownership_level = value

    def _adjust_ownership(self, owner: str, change: int):
        """
        Handle a player trying to capture (or reinforce ownership) of this game block.
        :param owner: Player requesting ownership
        :param change: Amount of ownership to give them
        """
        if owner != self.owner:
            self.ownership_level -= change
        else:
            self.ownership_level += change

        if self.ownership_level < 0:
            self.owner = owner

    def handle_ownership_message(self, message: messages.ClaimOwnershipMessage):
        self._adjust_ownership(message.owner_id, 1)

    @property
    def destruction_level(self):
        return self._destruction_level

    @destruction_level.setter
    def destruction_level(self, value):
        if value > self._destruction_threshold:
            self.terminate()
        if value < 0:
            value = 0

        self._destruction_level = value

    def handle_destroy_message(self, message: messages.DestroyMessage):
        self.destruction_level += 1

    def handle_repair_message(self, message: messages.RepairMessage):
        self.destruction_level -= 1

    def terminate(self):
        """
        This block has been destroyed. Notify manager and expect to be terminated.
        """
        self.send_message_to_manager(messages.TerminationRequestMessage())

    def handle_query_message(self, message: messages.QueryStatusMessage):
        """
        When receiving a query message, respond to it with the current owner, ownership level and destruction level.
        :param message:
        :return:
        """
        response = messages.QueryResponseMessage(self.owner, self.ownership_level, self.destruction_level)
        self.reply_to_message(message, response)
            
    def receive_message(self, message: messages.BaseMessage):
        """
        All messages pass through here. If it's an action message then ask the game manager to validate it. If it's
        invalid, then the message is silently dropped.
        :param message:
        """
        if issubclass(message, messages.BaseActionMessage):
            if not self.validate_action(message):
                return
        super(TargettableBlock, self).receive_message(message)

    def validate_action(self, message: messages.BaseActionMessage) -> bool:
        """
        Strip the solved work out of a given action message and send it to the game manager to validate it.

        This function is blocking until a validation response is received.
        :param message:
        :return: True if manager validates the work. False otherwise.
        """
        self._awaiting_validation = True
        self._action_validated = False
        new_message = messages.ValidateActionMessage()
        new_message.worker_id = message.worker_id
        new_message.guess = message.guess
        new_message.nonce = message.nonce
        self.send_message_to_manager(new_message)

        while self._awaiting_validation:
            time.sleep(self._validation_poll_interval)

        return self._action_validated

    def handle_action_validated_message(self, message: messages.BaseMessage):
        """
        Only expect to receive this while :func:`~TargettableBlock.validate_action` is blocking.
        Receiving this means that the game manager thinks the work solution sent to it is correct.
        :param message:
        """
        self._awaiting_validation = False
        self._action_validated = True

    def handle_action_invalidated_message(self, message: messages.BaseMessage):
        """
        Only expect to receive this while :func:`~TargettableBlock.validate_action` is blocking.
        Receiving this means that the game manager thinks the work solution sent to it is incorrect.
        :param message:
        """
        self._awaiting_validation = False
        self._action_validated = False
