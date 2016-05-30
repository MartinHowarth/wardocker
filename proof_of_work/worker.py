import time
import hashlib
from struct import unpack, pack
from ..communication import messages


class Worker:
    def __init__(self, manager_contact_function):
        self.worker_id = None
        self.manager_contact_function = manager_contact_function
        self.payload = None
        self.target_maximum = None
        self.guess = None
        self.nonce = None
        self._last_work_time = 0

        self.request_work_id()

    def request_work_id(self):
        message = messages.RequestWorkerIdMessage()
        self.manager_contact_function(message)

    def receive_work_id(self, message: messages.ProvideWorkerIdMessage):
        self.worker_id = message.worker_id

    def request_work(self):
        message = messages.RequestWorkMessage(self.worker_id)
        self.manager_contact_function(message)
        # self.payload, self.target = self.work_manager.request_work(self.worker_id)

    def receive_work(self, message: messages.ProvideWorkMessage):
        self.payload = message.payload
        self.target_maximum = message.target_maximum

    def do_work(self):
        if self.payload is None:
            return False

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
        return True

    def submit_work(self):
        message = messages.SubmitWorkMessage(self.worker_id, self.guess, self.nonce)
        self.manager_contact_function(message)
        # if self.work_manager.submit_work(self.worker_id, self.guess, self.nonce):
        #     print("Success")
        # else:
        #     print("Failure")
