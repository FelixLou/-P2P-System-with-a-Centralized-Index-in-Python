from thread import *
from socket import *


version = "P2P-CI/1.0"
status = "200 OK"

def handle_client(connectionSocket):
	while(1):
		try:
			print "try"
			s = connectionSocket.recv(1024) 
			s = s.splitlines()
			print s
			first_line = s[0].split()
			if(len(first_line) < 4):
				if(first_line[2] != version):
					connectionSocket.send("500 P2P-CI Version Not Supported")
					continue
			elif(first_line[3] != version):
				connectionSocket.send("500 P2P-CI Version Not Supported")
				continue
			
			'''
		    for ip in peers[::2]:
				if(ip == second_line[1]):
					exist = true
					break 

			'''
			second_line = s[1].split()
			third_line = s[2].split()
			
			if len(s) > 3:
				#print "length"
				forth_line = s[3].split()
				#print forth_line
			
			#add a peer
			if(first_line[0].lower() == "reg"):
				print "test3"
				peers.insert(0,second_line[1])#IP address
				peers.insert(1,third_line[1])#port number
				print "length:",len(peers)
				connectionSocket.send("Successfully register this computer")
				continue
			print "test4"
			'''	
			if(~exist):
				peers.insert(second_line[1], 0)#IP address
				peers.insert(third_line[1], 1)#port number
				print "add"   
			'''

			if(first_line[0].lower() == "add"):
				rfcs.insert(0,first_line[2])#RFC number
				rfcs.insert(1,forth_line[1])#title
				rfcs.insert(2,second_line[1])#ip address
				add_info = version + " "+ status + "\n"
				add_info += "RFC "+first_line[2]+ " "+ forth_line[1]+" "+third_line[1]
				connectionSocket.send(add_info)
			elif(first_line[0].lower() == "lookup"):
				rfc_info = version + " "+ status
				rfcs_len = len(rfcs)
				print first_line[2]
				for i in xrange(0,rfcs_len,3):
					if(first_line[2] == rfcs[i]):
						rfc_info += "RFC "+ rfcs[i]+" "+rfcs[i + 2]+ " " +  "\n"
				if(rfc_info == version + " "+ status):
					connectionSocket.send(version + " 404 Not Found")
				else:
					connectionSocket.send(rfc_info)
			elif(first_line[0].lower() == "list"):
				rfcs_info = version + " "+ status + "\n"
				rfcs_len = len(rfcs)
				for i in xrange(0,rfcs_len,3):
					rfcs_info +="RFC "+ rfcs[i]+" "+rfcs[i+1]+" "+rfcs[i + 2]+ "\n"
				connectionSocket.send(rfcs_info)
			else:
				connectionSocket.send(version + "400 Bad Request")
		except:
			#print first_line[0].lower()

			#remove RFCs this peer has in rfcs
			rfcs_len = len(rfcs)
			
			print "before: ",rfcs_len
			for i in xrange(len(rfcs)-1,1,-3):
				print "iiii:", i
				if(second_line[1]== rfcs[i]): #ip address
					print "i:", i 
					rfcs.pop(i)
					rfcs.pop(i -1)
					rfcs.pop(i -2)
			#remove this peer from peers
			print "before: ",len(peers)
			index = peers.index(second_line[1]) #ip address
			peers.remove(second_line[1])
			peers.pop(index)

			connectionSocket.close()
			print "after: ",len(peers)
			print len(rfcs)
			return

serverPort = 7734
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort)) 
serverSocket.listen(1)
print 'The server is ready to receive'
peers = []; #initiate a list of peers
rfcs = []; #initiate a list of RCFs
while 1:
	connectionSocket, addr = serverSocket.accept()
	start_new_thread(handle_client, (connectionSocket,))




