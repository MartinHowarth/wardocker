import logging
import http.server
import socketserver
import threading
from . import messages


class MyBaseRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, action_mapping: dict=None, *args, **kwargs):
        self.action_mapping = action_mapping
        super(MyBaseRequestHandler, self).__init__(*args, **kwargs)

    @classmethod
    def specify_action_mapping(cls, action_mapping):
        def create_handler(*args, **kwargs):
            return cls(action_mapping, *args, **kwargs)
        return create_handler

    def respond_ok(self):
        self.send_response(http.server.HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        """
        Receive and handle a POST message.
        :return:
        """
        self.respond_ok()
        data_string = self.rfile.read(int(self.headers['Content-Length']))

        logging.info("Received raw POST data: %s" % data_string)
        message = messages.parse_raw_message(data_string)
        self.handle_request(message)

    def handle_request(self, message: messages.BaseMessage):
        self.action_mapping[message.message_type](message)


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
