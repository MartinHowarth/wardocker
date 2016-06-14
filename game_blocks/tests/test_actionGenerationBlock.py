from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock
from game_blocks.action_generation_block import ActionGenerationBlock
from communication import messages


class TestActionGenerationBlock(TestCase):
    def setUp(self):
        self.send_message_to_manager = MagicMock()
        self.action_generation_block = ActionGenerationBlock()
        self.action_generation_block.send_message_to_manager = self.send_message_to_manager

    def test_perform_action(self):
        self.fail()

    def test_request_work(self):
        self.fail()

    def test_receive_work(self):
        self.fail()

    def test_request_worker_id(self):
        self.assertIsInstance(self.send_message_to_manager.call_args[0][0], messages.RequestWorkerIdMessage)

    def test_receive_worker_id(self):
        self.fail()

    def test_add_work_to_message(self):
        self.fail()
