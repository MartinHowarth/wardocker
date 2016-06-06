import time
import hashlib
from struct import unpack, pack
from communication import messages


class Worker:
    _work_poll_interval = 0.1

    def __init__(self, manager_contact_function: callable):
        """
        :param manager_contact_function: Method to use to send messages to the work manager.
        """
        self.worker_id = None
        self.manager_contact_function = manager_contact_function
        self.payload = None
        self.target_maximum = None
        self.guess = None
        self.nonce = None
        self._last_work_time = 0
        self._awaiting_work = False

        self.request_work_id()

    def request_work_id(self):
        message = messages.RequestWorkerIdMessage()
        self.manager_contact_function(message)

    def receive_work_id(self, message: messages.ProvideWorkerIdMessage):
        self.worker_id = message.worker_id

    def request_work(self):
        """
        Ask the work manager for a task.
        Blocking until a task is received.
        """
        self._awaiting_work = True
        message = messages.RequestWorkMessage(self.worker_id)
        self.manager_contact_function(message)

        while self._awaiting_work:
            time.sleep(self._work_poll_interval)

    def receive_work(self, message: messages.ProvideWorkMessage):
        """
        Receive a task.
        Unblocks :func:`~Worker.request_work`
        :param message: Message containing the work task.
        """
        self.payload = message.payload
        self.target_maximum = message.target_maximum
        self._awaiting_work = False

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

    def add_work_to_message(self, message: messages.BaseActionMessage):
        """
        Add the last task solution and our ID to a given action message.
        This allows the recipient of the action message to verify our work.
        :param message:
        """
        message.worker_id = self.worker_id
        message.guess = self.guess
        message.nonce = self.nonce
