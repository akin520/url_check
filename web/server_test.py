#!/usr/bin/env python

import msgpackrpc

client = msgpackrpc.Client(msgpackrpc.Address("localhost", 18800))
result = client.call('getalldomain')
print result,type(result)
