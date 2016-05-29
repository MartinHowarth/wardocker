import time
import hashlib
from struct import unpack, pack


def verify_work(payload, guess, nonce):
    return unpack('>Q', hashlib.sha512(hashlib.sha512(pack('>Q', nonce) + payload).digest()).digest()[0:8])[0] == guess


class WorkManager:
    _worker_count = 0
    workers = {}

    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.message = "Congratulations, you found an Easter egg. Have a cookie."
        self.target = 2**64 / difficulty

    def _generate_payload(self):
        payload = (str(time.time()) + self.message).encode()
        return hashlib.sha512(payload).digest()

    def request_worker_id(self):
        self._worker_count += 1
        return self._worker_count

    def request_work(self, worker_id=None):
        if not worker_id:
            return None, None

        # Only allow each worker to have once workload at a time
        if worker_id in self.workers.keys():
            return None, None

        payload = self._generate_payload()
        self.workers[worker_id] = payload
        return payload, self.target

    def submit_work(self, worker_id, guess, nonce):
        payload = self.workers[worker_id]
        if verify_work(payload, guess, nonce):
            # Clear them from the current worker list
            del self.workers[worker_id]
            return True
        else:
            return False


class WorkTicket:
    def __init__(self, payload, target):
        self.payload = payload
        self.target = target
