import Pyro4
from game_blocks import base_block
from proof_of_work import manager


class ManagerBlock(base_block.BaseBlock):
    def __init__(self):
        self.target = ""
        super(ManagerBlock, self).__init__()

        self.work_manager = manager.WorkManager(10000)

        daemon = Pyro4.Daemon()
        ns = Pyro4.locateNS()  # find the name server
        uri = daemon.register(self.work_manager)  # register the work manager as a Pyro object
        ns.register("manager.work_manager", uri)

        daemon.requestLoop()                   # start the event loop of the server to wait for calls