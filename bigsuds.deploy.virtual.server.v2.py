#!/usr/bin/python
# -*- coding: UTF-8 -*-

import bigsuds
import pprint
import traceback

bigip_host = '192.168.76.101'
bigip_username = 'admin'
bigip_password = 'admin'


bigip = bigsuds.BIGIP(hostname = bigip_host)
onboarding_info = {
	"vlans" : ['external','internal','ha'],
	"vlan_ids" : [0,0,0],
	"members": [ 
					[{'member_name': '1.1', 'member_type': 'MEMBER_INTERFACE', 'tag_state': 'MEMBER_UNTAGGED'}],
                    [{'member_name': '1.2', 'member_type': 'MEMBER_INTERFACE', 'tag_state': 'MEMBER_UNTAGGED'}],
                    [{'member_name': '1.3', 'member_type': 'MEMBER_INTERFACE', 'tag_state': 'MEMBER_UNTAGGED'}]
               ],
	"failsafe_states" : ['STATE_DISABLED','STATE_DISABLED','STATE_DISABLED'],
    "timeouts" : [90,90,90],
    "self_ips" : ['10.1.1.1','110.1.1.1','200.200.200.1'],
    "vlan_names" : ['external','internal','ha'],
    "addresses" : ['10.1.1.1','110.1.1.1','200.200.200.1'],
    "netmasks" : ['255.255.0.0','255.255.0.0','255.255.255.0'],
    "traffic_groups" : ['traffic-group-local-only','traffic-group-local-only','traffic-group-local-only'],
    "floating_states" : ['STATE_DISABLED','STATE_DISABLED','STATE_DISABLED'],
	"default_route_names" : [ "default" ],
	"default_route_destinations" : [{'address':'0.0.0.0','netmask':'0.0.0.0'}],
	"default_route_gateways" : [{'gateway':'10.1.1.254'}]
					
}

virtual_server_config = {
	"pool" : { 
				"names": ['test-pool-1'],
			   	"lb_methods": ['LB_METHOD_ROUND_ROBIN'],
			   	"members":[[{'address':'110.1.1.129','port':80},{'address':'110.1.1.130','port':80}]],
			   	"monitor_rule" : {
                                   'type':'MONITOR_RULE_TYPE_AND_LIST',
                                   'quorum':0,
                                   'monitor_templates':['tcp']
                                 } 
			}
}

def bigip_onboarding(info):
	try:
		#create VLAN
		bigip.Networking.VLAN.create_v2(vlans = info["vlans"],
										vlan_ids = info["vlan_ids"],
										members = info["members"],
										failsafe_states = info["failsafe_states"],
										timeouts = info["timeouts"])
		
		#create SelfIP
		bigip.Networking.SelfIPV2.create(
								self_ips = info["self_ips"],
								vlan_names = info["vlan_names"],
								addresses = info["addresses"],
								netmasks = info["netmasks"],
								traffic_groups = info["traffic_groups"],
								floating_states = info["floating_states"])
	
		bigip.Networking.RouteTableV2.create_static_route(routes = info["default_route_names"],
													  destinations = info["default_route_destinations"],
													  attributes = info["default_route_gateways"])
		return True
	except Exception as e:
		print "do some exception process"
		pprint.pprint(e)
		return False
		
	
def create_pool():
	#create pool
	bigip.LocalLB.Pool.create_v2(pool_names = ['test-pool-1'],
								 lb_methods = ['LB_METHOD_ROUND_ROBIN'],
								 members = [[{'address':'110.1.1.129','port':80},{'address':'110.1.1.130','port':80}]])
	
	#assign monitor
	bigip.LocalLB.Pool.set_monitor_association( monitor_associations = [
												 {
													'pool_name':'test-pool-1',
											     	'monitor_rule': {
	                    											'type':'MONITOR_RULE_TYPE_AND_LIST',
	 																'quorum':0, 
																	'monitor_templates':['tcp']
																 	}
												}])


def create_vs():
	#create virtual server
	#bigip.LocalLB.VirtualServer.create( definitions = [{'name':'test-vs-1','address':'10.1.1.100', 'port':80, 'protocol': 'PROTOCOL_TCP'}],
	#							    wildmasks = ['255.255.255.255'],
	#							    resources = [{'type':'RESOURCE_TYPE_POOL','default_pool_name':'test-pool-1'}],
	#						        profiles = [
	#											 [
	#												{'profile_context':'PROFILE_CONTEXT_TYPE_ALL','profile_name':'tcp'},
	#												{'profile_context':'PROFILE_CONTEXT_TYPE_ALL','profile_name':'http'}
 	#											 ]
	#										   ])

	#set automap for the virtual server
	bigip.LocalLB.VirtualServer.set_snat_automap(['test-vs-1'])


if __name__ == '__main__':
	bigip_host = '192.168.76.101'
	bigip_username = 'admin'
	bigip_password = 'admin'

	bigip = bigsuds.BIGIP(hostname = bigip_host)
	bigip_onboarding(onboarding_info)
	create_pool()
	from vsconfig import *
	bigip.LocalLB.VirtualServer.create(**vs_config)
