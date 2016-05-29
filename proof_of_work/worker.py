import time
import hashlib
from struct import unpack, pack
from . import manager


class Worker:
    def __init__(self, work_manager: manager.WorkManager):
        self.work_manager = work_manager
        self.worker_id = self.work_manager.request_worker_id()
        self.payload = None
        self.target = None
        self.guess = None
        self.nonce = None
        self._last_work_time = 0

    def request_work(self):
        self.payload, self.target = self.work_manager.request_work(self.worker_id)

    def do_work(self):
        if self.payload is None:
            return False

        start_time = time.time()
        guess = 99999999999999999999
        nonce = 0
        payload = self.payload
        while guess > self.target:
            nonce += 1
            guess, = unpack('>Q', hashlib.sha512(hashlib.sha512(pack('>Q', nonce) + payload).digest()).digest()[0:8])

        end_time = time.time()
        self.nonce = nonce
        self.guess = guess
        self._last_work_time = end_time - start_time
        return True

    def submit_work(self):
        if self.work_manager.submit_work(self.worker_id, self.guess, self.nonce):
            print("Success")
        else:
            print("Failure")
