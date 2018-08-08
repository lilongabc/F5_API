vs_config = { 
		"definitions" : [{'name':'test-vs-100','address':'10.1.1.200', 'port':80, 'protocol': 'PROTOCOL_TCP'}],
		"wildmasks" : ['255.255.255.255'],
		"resources" : [{'type':'RESOURCE_TYPE_POOL','default_pool_name':'test-pool-1'}],
		"profiles" : [
			 [
				{'profile_context':'PROFILE_CONTEXT_TYPE_ALL','profile_name':'tcp'},
				{'profile_context':'PROFILE_CONTEXT_TYPE_ALL','profile_name':'http'}
			 ]
		   ]
} 
