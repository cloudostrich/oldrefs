"""
import win32ui
import dde

function getDataViaDDE(myRequests)
	server = dde.CreateServer()
	server.Create('MyDataProxy')
	conversation = dde.CreateConversation(server)
	conversation.ConnectTo("DDEServiceName", "DataTopic")

	myResults = {}
	for request in myRequests
		 myResults[request] = conversation.Request(request)
	
	return myResults
---------------------------------------------------------	
"""	
import dde
server = dde.CreateServer()
server.Create('')
conversation = dde.CreateConversation(self.server)
conversation.ConnectTo(application, service)
"-------------------------------------------------------"

import win32ui
import dde

server = dde.CreateServer()
server.Create("TestClient")

conversation = dde.CreateConversation(server)

conversation.ConnectTo("RunAny", "RunAnyCommand")
conversation.Exec("DoSomething")
conversation.Exec("DoSomethingElse")

conversation.ConnectTo("RunAny", "ComputeStringLength")
s = 'abcdefghi'
sl = conversation.Request(s)
print 'length of "%s" is %s'%(s,sl)
