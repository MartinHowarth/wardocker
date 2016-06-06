import logging
import http.server
import socketserver
import threading
from communication import messages


class MyBaseRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, target_method: callable=None, *args, **kwargs):
        self.target_method = target_method
        super(MyBaseRequestHandler, self).__init__(*args, **kwargs)

    @classmethod
    def specify_target_method(cls, target_method):
        def create_handler(*args, **kwargs):
            return cls(target_method, *args, **kwargs)
        return create_handler

    def respond_ok(self):
        self.send_response(http.server.HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Receive and handle a POST message.

        Expectation is that the POST will contain a JSON encoded dictionary representing a game message.

        When the message has been parsed, call the method specified at instantiation time with the message as the
        only parameter.
        """
        self.respond_ok()
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        logging.info("Received raw POST data: %s" % data_string)
        message = messages.parse_raw_message(data_string)
        message.from_address = ':'.join(self.client_address)
        self.target_method(message)


class BaseServer:
    def __init__(self, request_handler: MyBaseRequestHandler, port=80):
        self._port = port
        self._handler_class = request_handler
        self.http_daemon = socketserver.TCPServer(("", self._port), self._handler_class)
        self.server_thread = threading.Thread(target=self.http_daemon.serve_forever)
        self.server_thread.start()

    def end(self):
        self.http_daemon.shutdown()
        self.server_thread.join()
