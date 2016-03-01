## Synopsis

Project to help in the migration from Cisco ACE to F5 LTM, all nodes, pools and virtual servers can be migrated to tmsh syntax.

## Code Example

`convert.py ace_config.txt `

Creates a file in the same directory with the configuration of the LTM ready to paste in the tmsh cli.

`convert.py ace_config.txt -c`

Provides the number of nodes, pools and virtual servers in the ACE configuration.

## Motivation

Assists in the initial migration from Cisco ACE to LTM.

## Requirements

- [CiscoConfParse](http://www.pennington.net/py/ciscoconfparse/)