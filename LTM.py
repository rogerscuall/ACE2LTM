__author__ = 'rgomez'
from ace_parser import ACE


class LTM():
    def __init__(self):
        self.partition = 'Common'
        self.route_domain = '0'
        self.name = ''



class Monitor(LTM):
    def __init__(self):
        self.protocol = ''
        self.port = ''



class Node(LTM):
    def __init__(self):
        self.ip = ''
        self.monitor = ''



class Pool(LTM):
    def __init__(self):
        self.nodes = []
        self.monitor = ''


class Member(Node):
    def __init__(self):
        Node.__init__(self)
        self.port = ''


class Virtual_Server(LTM):
    def __init__(self):
        self.pool = ''
        self.ip = ''
        self.port = ''
        self.protocol = ''


