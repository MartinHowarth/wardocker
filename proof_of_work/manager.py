import time
import hashlib
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

    def request_worker_id(self) -> int:
        """
        Generate and return a unique worker id.
        :return: Unique worker ID.
        """
        self._worker_count += 1
        return self._worker_count

    def request_work(self, worker_id: int) -> (bytes, int):
        """
        Get and return a work task.
        Each worker is only allowed one task at once.
        A task consists of a payload, and the target maximum value.
        :param worker_id: ID of worker requesting work.
        :return: Work task.
        """
        # Only allow each worker to have once workload at a time
        if worker_id in self.workers.keys():
            return None, None

        payload = self._generate_payload()
        self.workers[worker_id] = payload
        return payload, self.target_maximum

    def validate_work(self, worker_id: int, guess: int, nonce: int) -> bool:
        """
        Check that the given solution to a task correctly solves the task given to that worker.
        :param worker_id: ID of worker who solved the task
        :param guess: See
        :param nonce:
        :return:
        """
        payload = self.workers[worker_id]
        if verify_payload(payload, guess, nonce):
            # Clear them from the current worker-task mapping.
            del self.workers[worker_id]
            return True
        else:
            return False
