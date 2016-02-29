## Synopsis

Project to help in the migration from Cisco ACE to F5 LTM, all nodes, pools and virtual servers can be migrated to tmsh syntax. Also some counts of the number of objects can be done.

## Code Example

`convert.py ace_config.txt `

Will create file in the same directory with the configuration of the LTM ready to paste in the tmsh cli.

`convert.py ace_config.txt -c"`

Provide the number of nodes, pools and virtual servers in the ACE configuration.

## Motivation

Assist in the initial migration from Cisco ACE to LTM.

## Requirements

- [CiscoConfParse](http://www.pennington.net/py/ciscoconfparse/)