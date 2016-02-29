__author__ = 'Roger Gomez'
from LTM import *
__author__ = 'rgomez'



file = '/Users/rgomez/OneDrive/Programs/ACE2LTM/ace.txt'


class LTMConfig:
    def __init__(self):
        self.monitors = {}
        self.nodes = {}
        self.pools = {}
        self.virtual_server = {}

    def ace_ltm(self, file):
        config = ACE(file)
        config.update_config()
        monitor_list = config.probes
        for i in monitor_list:
            monitor = Monitor()
            monitor.name = i
            monitor.protocol = monitor_list[i]['protocol']
            monitor.port = monitor_list[i]['port']
            self.monitors[i] = monitor
        node_list = config.rservers
        for key, value in node_list.iteritems():
            node = Node()
            node.name = key
            node.ip = value
            self.nodes[key] = node
        pool_list = config.serverfarm
        for key, value in pool_list.iteritems():
            pool = Pool()
            pool.name = key
            pool.nodes = value['nodes']
            pool.monitor = value['probe']
            self.pools[key] = pool
        virtual_server_list = config.virtual_server
        for key, value in virtual_server_list.iteritems():
            virtual_server = Virtual_Server()
            virtual_server.name = key
            virtual_server.ip = value['ip']
            virtual_server.protocol = value['protocol']
            virtual_server.port = value['port']
            virtual_server.pool = value['pool']
            self.virtual_server[key] = virtual_server
