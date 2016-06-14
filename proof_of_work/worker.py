import time
import hashlib
from struct import unpack, pack


class Worker:
    def __init__(self):
        self.worker_id = None
        self.payload = None
        self.target_maximum = None
        self.guess = None
        self.nonce = None
        self._last_work_time = 0

    def receive_work_id(self, worker_id: int):
        self.worker_id = worker_id

    def receive_work(self, payload: bytes, target_maximum: int):
        """
        Receive a task.
        Unblocks :func:`~Worker.request_work`
        :param payload: Payload of the work to be solved.
        :param target_maximum: Target maximum of the work to be solved (determines difficulty).
        """
        self.payload = payload
        self.target_maximum = target_maximum

    def do_work(self):
        """
        Actually work out the solution to the task set.
        """
        if self.payload is None or self.target_maximum is None:
            return

        start_time = time.time()
        guess = 99999999999999999999
        nonce = 0
        payload = self.payload
        while guess > self.target_maximum:
            nonce += 1
            guess, = unpack('>Q', hashlib.sha512(hashlib.sha512(pack('>Q', nonce) + payload).digest()).digest()[0:8])

        end_time = time.time()
        self.nonce = nonce
        self.guess = guess
        self._last_work_time = end_time - start_time
