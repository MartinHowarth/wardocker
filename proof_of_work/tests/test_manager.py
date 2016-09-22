from unittest import TestCase
from unittest.mock import patch
from proof_of_work.manager import WorkManager


@patch('time.time', return_value=0)
class TestWorkManager(TestCase):
    def setUp(self):
        self.manager = WorkManager(10)

    def test_request_worker_id(self, mocked_time):
        self.assertEqual(self.manager.request_worker_id(), 1)

    def test_request_work(self, mocked_time):
        worker_id = 100
        payload, target_maximum = self.manager.request_work(worker_id)
        self.assertEqual(payload, b'\xfb(z(0\xf5\xac<d\x88\x0e\xd2\r\x1d\xcce\x9d\x89WQY\x13\x0f\xb4\x19,\x89\x9dc)\x00'
                                  b'<A\xf4\xdev\xe3\\)\x80\x90\x06\x7f\xb0v\x86\xd7\xb8\xcd\x02\xact\xb7\xd3g,\x10\x8eD'
                                  b'\x8b\x9d7\x16E')
        self.assertEqual(target_maximum, 1.8446744073709553e+18)
        self.assertIn(worker_id, self.manager.workers)
        self.assertEqual(self.manager.workers[worker_id], payload)

    def test_validate_work(self, mocked_time):
        worker_id = 100
        payload, target_maximum = self.manager.request_work(worker_id)
        self.assertEqual(self.manager.validate_work(1, 0, 0), False)  # Test invalid worker id
        self.assertEqual(self.manager.validate_work(100, 0, 0), False)  # Test invalid work result
        self.assertEqual(self.manager.validate_work(100, 1624637542437931938, 7), True)  # Test valid result
