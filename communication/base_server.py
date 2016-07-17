import logging
import http.server
import socketserver
import threading
from communication import messages
import json


class MyBaseRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, target_method: callable=None, *args, **kwargs):
        self.target_method = target_method
        super(MyBaseRequestHandler, self).__init__(*args, **kwargs)

    @classmethod
    def specify_target_method(cls, target_method):
        def create_handler(*args, **kwargs):
            return cls(target_method, *args, **kwargs)
        return create_handler

    def respond(self, response):
        print("Responding with: %s" % response)
        self.send_response(response)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Receive and handle a POST message.

        Expectation is that the POST will contain a JSON encoded dictionary representing a game message.

        When the message has been parsed, call the method specified at instantiation time with the message as the
        only parameter.
        """
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        logging.info("Received raw POST data: %s" % data_string)
        message = json.loads(data_string.decode('utf-8'))
        response = self.target_method(message)
        if response is None:
            response = http.server.HTTPStatus.OK
        self.respond(response)


class BaseServer:
    def __init__(self, request_handler: MyBaseRequestHandler):
        self._port = 8000
        self._handler_class = request_handler
        self.http_daemon = socketserver.TCPServer(("", self._port), self._handler_class)
        self.server_thread = threading.Thread(target=self.http_daemon.serve_forever)
        self.server_thread.start()

    def end(self):
        self.http_daemon.shutdown()
        self.server_thread.join()
