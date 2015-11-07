from thread import *
from socket import *
from sys import *
import threading
import time
import os

class Peers(threading.Thread):
	def __init__(self,connectionSocket):
		super(Peers, self).__init__()
		self.connectionSocket = connectionSocket
	
	def run(self):
#def handle_client(connectionSocket):
		while(1):
			try:
				s = self.connectionSocket.recv(1024) 
				s = s.splitlines()
				first_line = s[0].split()
				if(len(first_line) < 4):
					if(first_line[2] != version):
						self.connectionSocket.send("500 P2P-CI Version Not Supported")
						continue
				elif(first_line[3] != version):
					self.connectionSocket.send("500 P2P-CI Version Not Supported")
					continue
				second_line = s[1].split()
				third_line = s[2].split()
				
				if len(s) > 3:
					forth_line = s[3].split()
				
				#add a peer
				if(first_line[0].lower() == "reg"):
					peers.insert(0,second_line[1])#IP address
					peers.insert(1,third_line[1])#port number
					self.connectionSocket.send("Successfully register this computer")
					continue

				if(first_line[0].lower() == "add"):
					rfcs.insert(0,first_line[2])#RFC number
					rfcs.insert(1," ".join(forth_line[1:]))#title
					rfcs.insert(2,second_line[1])#ip address
					add_info = version + " "+ status + "\n"
					add_info += "RFC "+rfcs[0]+ " "+ rfcs[1]+" "+rfcs[2]
					self.connectionSocket.send(add_info)
				elif(first_line[0].lower() == "lookup"):
					rfc_info = version + " "+ status
					rfcs_len = len(rfcs)
					
					for i in xrange(0,rfcs_len,3):
						#if rfc number
						if(first_line[2] == rfcs[i]):
							#ipaddress_index + 1 is the peer's port number 
							port_number_index = peers.index(rfcs[i + 2]) + 1
							rfc_info += "\n" + "RFC "+ rfcs[i]+" "+rfcs[i + 2]+ " " + peers[port_number_index]
					if(rfc_info == version + " "+ status):
						self.connectionSocket.send(version + " 404 Not Found")
					else:
						self.connectionSocket.send(rfc_info)
				elif(first_line[0].lower() == "list"):
					
					rfcs_info = version + " "+ status + "\n"
					rfcs_len = len(rfcs)
					
					for i in xrange(0,rfcs_len,3):
						rfcs_info +="RFC "+ rfcs[i]+" "+rfcs[i+1]+" "+rfcs[i + 2]+ "\n"
		
					self.connectionSocket.send(rfcs_info)
				elif(first_line[0].lower() == "disconnect"):

					#remove RFCs this peer has in rfcs
					rfcs_len = len(rfcs)
					
					for i in xrange(len(rfcs)-1,1,-3):
						
						if(second_line[1]== rfcs[i]): #ip address
							rfcs.pop(i)
							rfcs.pop(i -1)
							rfcs.pop(i -2)
					#remove this peer from peers
					
					index = peers.index(second_line[1]) #ip address
					peers.remove(second_line[1])
					peers.pop(index)

					self.connectionSocket.close()
					return
				else:
					self.connectionSocket.send(version + "400 Bad Request")
			except:
					print("except")

class Command(threading.Thread):
	def run(self):
		while True:
			command = raw_input('Waiting for command:')
			if(command == 'quit' or command == 'q'):
				 os._exit(1)

version = "P2P-CI/1.0"
status = "200 OK"
serverPort = 7734
serverSocket = socket(AF_INET,SOCK_STREAM) 
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('',serverPort)) 
serverSocket.listen(1)
print 'The server is ready to receive'
peers = []; #initiate a list of peers
rfcs = []; #initiate a list of RCFs
waitForCommand = Command()
waitForCommand.start()
while 1:
	connectionSocket, addr = serverSocket.accept()
	#start_new_thread(handle_client, (connectionSocket,))
	talkWithPeers = Peers(connectionSocket)
	talkWithPeers.start()

	




