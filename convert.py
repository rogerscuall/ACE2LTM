#!/usr/bin/env python
__author__ = 'Roger Gomez'

import argparse
from ace_parser import *

def main():
    """
    Script to find the number of objects inside ACE or convert the configuration to LTM
    :return: It can return the number of objects or a file with the configuration for LTM
    """
    parser = argparse.ArgumentParser(description="Convert ACE configuration to LTM")
    parser.add_argument("file", help="Location of the ACE configuration", type=str)
    parser.add_argument("-c", "--count", help="Number of objects in the configuration", action='store_true')
    cli_args = parser.parse_args()
    conf_file = cli_args.file
    conf_numbers = cli_args.count
    config = ACE(conf_file)
    config.update_config()

    if conf_numbers:
        print "Nodes: ", ACE._count_length(config.rservers)
        print "Pools: ", ACE._count_length(config.serverfarm)
        print "Virtual Servers: ", ACE._count_length(config.virtual_server)
    else:
        config.cli_to_file()

if __name__ == "__main__":
    main()

