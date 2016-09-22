from .base import BaseContainer


class PythonCommandContainer(BaseContainer):
    container_image_name = "python:3"
    entrypoint = "python -c"

    def __init__(self, client, command):
        self.command = command
        super(PythonCommandContainer, self).__init__(client)


class PythonModuleContainer(BaseContainer):
    container_image_name = "python:3"
    entrypoint = "python -m"

    def __init__(self, client, command):
        self.command = command
        super(PythonModuleContainer, self).__init__(client)


class PythonScriptContainer(BaseContainer):
    container_image_name = "python:3"
    entrypoint = "python"

    _container_python_directory = '/home/python_scripts/'

    def __init__(self, client, script_name, host_script_directory, *args, **kwargs):
        self.command = script_name
        self.command += ''.join([str(arg) for arg in args])
        self.command += ''.join(['--%s %s' % (key, value) for key, value in kwargs])
        self.command = self._container_python_directory + self.command
        binds = ['{}:{}'.format(host_script_directory, self._container_python_directory)]
        super(PythonScriptContainer, self).__init__(client, binds=binds)

