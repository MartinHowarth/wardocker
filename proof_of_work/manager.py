import time
import hashlib
from communication import messages
from struct import unpack, pack


def verify_payload(payload: bytes, guess: int, nonce: int):
    return unpack('>Q', hashlib.sha512(hashlib.sha512(pack('>Q', nonce) + payload).digest()).digest()[0:8])[0] == guess


class WorkManager:
    """
    Hands out tasks to workers. Tasks are hash-cracking exercises which are hard to solve, but easy to check.

    The task implementation here is based on https://www.cryptocoinsnews.com/proof-of-work/
    """
    _worker_count = 0
    workers = {}

    def __init__(self, difficulty: int):
        """
        :param difficulty: Higher difficulty means the work problems will take longer to solve.
        """
        self.difficulty = difficulty
        self.message = "Congratulations, you found an Easter egg. Have a cookie."
        self.target_maximum = 2 ** 64 / difficulty

    def _generate_payload(self) -> bytes:
        """
        Generate a unique payload.
        :return: Hash of a unique string.
        """
        payload = (str(time.time()) + self.message).encode()
        return hashlib.sha512(payload).digest()

    def request_worker_id(self, response_function: callable) -> \
            messages.ProvideWorkerIdMessage:
        """
        Generate and respond with a unique worker id.
        """
        self._worker_count += 1
        response_function(messages.ProvideWorkerIdMessage(self._worker_count))

    def request_work(self, message: messages.RequestWorkMessage, response_function: callable):
        """
        Get and return a work task.
        Each worker is only allowed one task at once.
        A task consists of a payload, and the target maximum value.
        """
        # Only allow each worker to have once workload at a time
        if message.worker_id in self.workers.keys():
            response_function(messages.ProvideWorkMessage(b'', 0))

        payload = self._generate_payload()
        self.workers[message.worker_id] = payload
        response_function(messages.ProvideWorkMessage(payload, self.target_maximum))

    def validate_work(self, message: messages.ValidateActionMessage, response_function: callable):
        """
        Check that the given solution to a task correctly solves the task given to that worker.
        """
        if message.worker_id not in self.workers.keys():
            response_function(messages.InvalidActionResponse())
        payload = self.workers[message.worker_id]
        if verify_payload(payload, message.guess, message.nonce):
            # Clear them from the current worker-task mapping.
            del self.workers[message.worker_id]
            response_function(messages.ValidActionResponse())
        else:
            response_function(messages.InvalidActionResponse())
