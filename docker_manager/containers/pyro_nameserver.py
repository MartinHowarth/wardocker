from .python import PythonModuleContainer


class PyroNameServer(PythonModuleContainer):
    def __init__(self, client, ip):
        super(PyroNameServer, self).__init__(client, "Pyro4.naming --host='%s'" % ip)
