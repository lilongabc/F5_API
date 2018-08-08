#!/usr/bin/python
# -*- coding: UTF-8 -*-

import bigsuds

bigip_host = '192.168.76.101'
bigip_username = 'admin'
bigip_password = 'admin'
bigip = bigsuds.BIGIP(hostname = bigip_host)
bigip.LocalLB.VirtualServer.delete_all_virtual_servers()
bigip.LocalLB.Pool.delete_all_pools()
#bigip.Networking.RouteTableV2.delete_static_route(['default'])
bigip.Networking.RouteTableV2.delete_all_static_routes()
bigip.Networking.SelfIPV2.delete_all_self_ips()
bigip.Networking.VLAN.delete_all_vlans()
