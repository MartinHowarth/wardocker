import time
import hashlib
import Pyro4
import base64
from struct import unpack, pack


@Pyro4.expose
class Worker:
    work_manager = Pyro4.Proxy("PYRONAME:manager.work_manager")

    def __init__(self):
        self.worker_id = None
        self.payload = None
        self.target_maximum = None
        self.guess = None
        self.nonce = None
        self._last_work_time = 0
        self._new_worker_id()

    def _new_worker_id(self):
        self.worker_id = self.work_manager.generate_worker_id()

    def get_work(self):
        """
        Receive a task.
        Unblocks :func:`~Worker.request_work`
        :param payload: Payload of the work to be solved.
        :param target_maximum: Target maximum of the work to be solved (determines difficulty).
        """
        payload, self.target_maximum = self.work_manager.generate_work(self.worker_id)

        # Pyro4 (via serpent serialiser, I think) returns bytes as a base64 encoded string
        #  - we need to convert it back
        self.payload = base64.b64decode(payload['data'])

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
