from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock
from proof_of_work.worker import Worker
from communication import messages
import hashlib


class TestWorker(TestCase):
    def setUp(self):
        self.mock_manager = MagicMock()
        self.worker = Worker(self.mock_manager)

    def test_request_work_id(self):
        self.assertIsInstance(self.mock_manager.call_args[0][0], messages.RequestWorkerIdMessage)

    def test_receive_work_id(self):
        message = messages.ProvideWorkerIdMessage(10)
        self.worker._new_worker_id(message)
        self.assertEqual(self.worker.worker_id, 10)

    def test_request_work(self):
        message = messages.ProvideWorkerIdMessage(10)
        self.worker._new_worker_id(message)
        # Make sure we don't get stuck waiting for work by forcing awaiting_work to be False.
        type(self.worker)._awaiting_work = PropertyMock(return_value=False)

        self.worker.request_work()
        self.assertIsInstance(self.mock_manager.call_args[0][0], messages.RequestWorkMessage)
        self.assertEqual(self.mock_manager.call_args[0][0].worker_id, 10)

    def test_receive_work(self):
        message = messages.ProvideWorkMessage(b"payload", 1000000)
        self.worker.get_work(message)
        self.assertEqual(self.worker.payload, b"payload")
        self.assertEqual(self.worker.target_maximum, 1000000)

    def test_do_work(self):
        payload = hashlib.sha512("test_message".encode()).digest()
        target_maximum = 2 ** 64 / 100

        self.worker.payload = payload
        self.worker.target_maximum = target_maximum

        self.worker.do_work()

        self.assertEqual(self.worker.nonce, 32)
        self.assertEqual(self.worker.guess, 120128094251766818)

    def test_add_work_to_message(self):
        self.worker.worker_id = 10
        self.worker.guess = 100
        self.worker.nonce = 1000

        message = messages.BaseActionMessage("")
        self.worker.add_work_to_message(message)

        self.assertEqual(message.worker_id, 10)
        self.assertEqual(message.guess, 100)
        self.assertEqual(message.nonce, 1000)
