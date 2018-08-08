#!/usr/bin/python

import bigsuds

# set target system and supply login info
b = bigsuds.BIGIP(
        hostname = '192.168.76.101',
        username = 'admin',
        password = 'admin',
        )

#make members
b.LocalLB.Pool.create_v2(
        pool_names = ['fake1'],
        lb_methods = ['LB_METHOD_ROUND_ROBIN'],
        members = [[
                {'address': '10.1.212.233', 'port': '80'},
                {'address': '10.1.212.234', 'port': '80'},
                {'address': '10.1.212.235', 'port': '80'},
                {'address': '10.1.212.236', 'port': '80'},
                {'address': '10.1.212.237', 'port': '80'}
                ]]
        )

