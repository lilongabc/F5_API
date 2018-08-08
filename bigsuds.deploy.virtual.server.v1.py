#!/usr/bin/python
# -*- coding: UTF-8 -*-

import bigsuds
import pprint

bigip_host = '192.168.76.101'
bigip_username = 'admin'
bigip_password = 'admin'


bigip = bigsuds.BIGIP(hostname = bigip_host)

#create VLAN
try:
	bigip.Networking.VLAN.create_v2(vlans = ['external','internal','ha'],
									vlan_ids = [0,0,0],
									members = [[{'member_name': '1.1', 'member_type': 'MEMBER_INTERFACE', 'tag_state': 'MEMBER_UNTAGGED'}],
											   [{'member_name': '1.2', 'member_type': 'MEMBER_INTERFACE', 'tag_state': 'MEMBER_UNTAGGED'}],
 											   [{'member_name': '1.3', 'member_type': 'MEMBER_INTERFACE', 'tag_state': 'MEMBER_UNTAGGED'}]
											  ],
									failsafe_states = ['STATE_DISABLED','STATE_DISABLED','STATE_DISABLED'],
									timeouts = [90,90,90])
except Exception as e:
	print "do some exception process"

#create SelfIP
bigip.Networking.SelfIPV2.create(
							self_ips = ['10.1.1.1','110.1.1.1','200.200.200.1'],
							vlan_names = ['external','internal','ha'],
							addresses = ['10.1.1.1','110.1.1.1','200.200.200.1'],
							netmasks = ['255.255.0.0','255.255.0.0','255.255.255.0'],
							traffic_groups = ['traffic-group-local-only','traffic-group-local-only','traffic-group-local-only'],
							floating_states = ['STATE_DISABLED','STATE_DISABLED','STATE_DISABLED'])

bigip.Networking.RouteTableV2.create_static_route(['default'],
												  [{'address':'0.0.0.0','netmask':'0.0.0.0'}],
												  [{'gateway':'10.1.1.254'}])

#create pool
bigip.LocalLB.Pool.create_v2(['test-pool-1'],
							 ['LB_METHOD_ROUND_ROBIN'],
							 [[{'address':'110.1.1.129','port':80},{'address':'110.1.1.130','port':80}]])

#assign monitor
bigip.LocalLB.Pool.set_monitor_association([{'pool_name':'test-pool-1',
										     'monitor_rule': {
                    											'type':'MONITOR_RULE_TYPE_AND_LIST',
 																'quorum':0, 
																'monitor_templates':['tcp']
															 }
											}])


#create virtual server
bigip.LocalLB.VirtualServer.create([{'name':'test-vs-1','address':'10.1.1.100', 'port':80, 'protocol': 'PROTOCOL_TCP'}],
								   ['255.255.255.255'],
								   [{'type':'RESOURCE_TYPE_POOL','default_pool_name':'test-pool-1'}],
							       [[{'profile_context':'PROFILE_CONTEXT_TYPE_ALL','profile_name':'tcp'},{'profile_context':'PROFILE_CONTEXT_TYPE_ALL','profile_name':'http'}]])

#set automap for the virtual server
bigip.LocalLB.VirtualServer.set_snat_automap(['test-vs-1'])
