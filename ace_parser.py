from ciscoconfparse import CiscoConfParse
#from __future__ import print_function
import sys

file = '/Users/rgomez/OneDrive/Programs/ACE2LTM/ace.txt'

class ACE():
    def __init__(self, file):
        """
        :param file:
        :self.rservers: a dictionary with key name of the RealServer and value IP_address
        :self.serverfarm: a dictionary with key name of the ServerFarm nested inside another dictionary with two keys,
        the value of the key nodes is a list , each element of that list a dictionary with the keys: name and port of
        the rserver.
        The second key inside ServerFarm is probe.
        {ServerFarm:{node:[{name: rserver, port: port], probe: probe_name}, ...}
        :self.probes: is a dictionary with key as name of the probe, in each key there is another dictionary with
        protocol and port information.
        {probe_name:{protocol: tcp, port: port}, ...}
        """
        self.parser = CiscoConfParse(file)
        self.rservers = {}
        self.serverfarm = {}
        self.probes = {}
        self.virtual_server = {}


    def set_rservers(self):
        list_rserver = self.parser.find_objects(r'^rserver host')
        for i in list_rserver:
            rserver = i.re_search_children('ip address')
            name_rserver = i.text.split(' ')[-1]
            if rserver == []:
                print("The Real Server {} don't have any IP".format(name_rserver))
            #is a list of only one element always
            rserver = rserver[0].text
            ip_rserver = rserver.split(' ')[-1]
            self.rservers[name_rserver] = ip_rserver

    def find_probe(self, probe_name):
        probe = self.parser.find_objects('^probe tcp' + " " + probe_name)
        probe = probe[0]
        probe_protocol = probe.text.split(' ')[-2]
        probe_name = probe.text.split(' ')[-1]
        probe_port = probe.re_search_children('port')
        probe_port = probe_port[0].text.split(' ')[-1]
        probe_dict = {'name': probe_name, 'protocol': probe_protocol, 'port': probe_port}
        return probe_dict



    def set_serverfarm(self):
        list_serverfarm = self.parser.find_objects(r'serverfarm host')
        for i in list_serverfarm:
            serverfarm_name = i.text.split(' ')[-1]
            probe = i.re_search_children('probe')
            #is a list of only one element always
            probe_name = probe[0].text.split(' ')[-1]
            probe = self.find_probe(probe_name)
            try:
                self.set_probes(probe)
            except IndexError as e:
                print('The probe {} was already added'.format(e[0]))
            list_rservers = i.re_search_children('rserver')
            temp_list = []
            for ii in list_rservers:
                rserver ={}
                rserver['name'] = (ii.text.split(' ')[-2])
                rserver['port'] = (ii.text.split(' ')[-1])
                temp_list.append(rserver)
            self.serverfarm[serverfarm_name] = {}
            self.serverfarm[serverfarm_name]['nodes'] = temp_list
            self.serverfarm[serverfarm_name]['probe'] = probe_name

    def set_virtual_server(self):
        list_virtual_server = self.parser.find_objects(r'class-map match-all')
        for i in list_virtual_server:
            virtual_server_name = i.text.split(' ')[-1]
            virtual_address = i.re_search_children(r'2 match virtual-address')
            #is a list of only one element always
            virtual_address = virtual_address[0].text
            virtual_address_port = virtual_address.split(' ')[-1]
            virtual_address_protocol = virtual_address.split(' ')[-3]
            virtual_address_ip = virtual_address.split(' ')[-4]
            parentspec = '^class '+ virtual_server_name + '$'
            policy = self.parser.find_objects_w_parents(parentspec=parentspec,
                                                       childspec='loadbalance policy')
            #is a list of only one element always
            try:
                policy = policy[0].text
                policy_name = policy.split(' ')[-1]
                #print policy_name
                parentspec = 'policy-map type loadbalance first-match ' + policy_name + '$'
                serverfarm = policy = self.parser.find_objects_w_parents(parentspec=parentspec,
                                                       childspec='serverfarm ')

                #is a list of only one element always
                serverfarm = serverfarm[0].text
                serverfarm_name = serverfarm.split(' ')[-1]
                self.virtual_server[virtual_server_name] = {'pool': serverfarm_name, 'ip': virtual_address_ip,
                                                            'port': virtual_address_port,
                                                            'protocol': virtual_address_protocol}
            except IndexError:
                print 'The policy-map type loadbalance with name {} was not found'.format(policy_name)



    def set_probes(self, probe):
        """
        :param probe: is a dictionary with format {'name': probe_name, 'protocol': probe_protocol, 'port': probe_port}
        :return: an Exception with two arguments is return if the probe already exist, first argument is the name of the
        probe and the second is an explanation string. If the value does not exist its added updating self.probes.
        """
        if self.probes.get(probe['name']):
            raise IndexError(probe['name'], 'Value exist already')
        else:
            self.probes[probe['name']] = {'port': probe['port'], 'protocol': probe['protocol']}


    def cli_add_probes(self):
        cli = 'create ltm monitor {} {} destination *:{}'
        for i in self.probes:
            print(cli.format(self.probes[i]['protocol'], i, self.probes[i]['port']))

    def cli_add_probes_to_pools(self):
        cli = 'modify ltm pool {} monitor {}'
        for i in self.serverfarm:
            if self.serverfarm[i]['probe'] == '80':
                print(cli.format(i, 'http'))
            else:
                print(cli.format(i, self.serverfarm[i]['probe']))

    def cli_add_nodes(self):
        cli = 'create ltm node {} address {}'
        for i in self.rservers:
            print(cli.format(i, self.rservers[i]))

    def cli_add_pools(self):
        cli = 'create ltm pool {}'
        for i in self.serverfarm:
            print(cli.format(i))

    def cli_add_virtual_servers(self):
        cli = 'create ltm virtual {} destination {}:{} ip-protocol {} pool {}'
        for i in self.virtual_server:
            print(cli.format(i, self.virtual_server[i]['ip'], self.virtual_server[i]['port'],
                             self.virtual_server[i]['protocol'], self.virtual_server[i]['pool']))

    def cli_add_node_to_pools(self):
        cli = 'modify ltm pool {} members add {{ {}:{} }}'
        for i in self.serverfarm:
            for ii in self.serverfarm[i]['nodes']:
                print(cli.format(i, ii['name'], ii['port']))


    def _count_length(self, atribute):
        return len(atribute)

    def cli_to_file(self):
        output = open('LTM-Config.txt', 'w')
        sys.stdout = output
        self.cli_add_probes()
        self.cli_add_nodes()
        self.cli_add_pools()
        self.cli_add_probes_to_pools()
        self.cli_add_node_to_pools()
        self.cli_add_virtual_servers()
        output.close()


    def update_config(self):
        self.set_rservers()
        self.set_serverfarm()
        self.set_virtual_server()

