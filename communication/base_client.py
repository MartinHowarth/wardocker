import requests
import logging
from . import base_message


class BaseClient:
    def __init__(self):
        pass

    def send_post(self, ip_port, message: base_message.BaseMessage):
        url = "http://" + str(ip_port)
        logging.info("Sending %s to %s." % (message.as_dict, url))
        requests.post(url=url, json=message.as_dict)
