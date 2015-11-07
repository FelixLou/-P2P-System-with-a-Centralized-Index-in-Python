from socket import*
import sys
#server.listen(UploadPort)
import socket
import os
import thread
import time
import threading

class peer_send(threading.Thread):
    def run(self):
        while True:
            Userinput = raw_input("\nWhich RFC you want? (eg: rfc132) (obtain the list by \"list\", exit with \"disconnect\")")
            if Userinput == "disconnect":
                '''
                Peer.sendto(Userinput, (ServerIP,ServerPort))
                print str(Userinput)
                '''
                #Peer.close()
                #sys.exit()
                stopped = threading.Event()
                #set a timer, after 10 seconds.. kill this loop
                time.sleep(3)
                threading.Timer(1, stopped.set).start()
                Peer.close()
                sys.exit()
            elif Userinput == "list":
                listmessage = "LIST ALL P2P-CI/1.0\nHost: " + str(myip) + "\nPort: " + str(UploadPort)
                Peer.sendto(listmessage, (ServerIP,ServerPort))
                Answer=Peer.recv(4096)
                print Answer
            elif Userinput == "add":
                RFCNumber = raw_input('RFC Number: ')
                listmessage = "ADD RFC " + RFCNumber + " P2P-CI/1.0\nHost: " + str(myip) + "\nPort: " + str(UploadPort)+ "\nTitle: " + RFCTitle  + "\n"
                Peer.sendto(listmessage, (ServerIP,ServerPort))
                Answer=Peer.recv(4096)
                print Answer
            elif Userinput == "lookup":
                RFCNumber = raw_input("What's the number of RFC you want check: ")
                lookupmessage = "LOOKUP RFC " + RFCNumber + " P2P-CI/1.0\nHost: " + str(myip)+ "\nPort: " + str(UploadPort) + "\nTitle: " + RFCTitle  + "\n"
                Peer.sendto(lookupmessage, (ServerIP,ServerPort))
                Answer=Peer.recv(4096)
                print Answer
            else:
                pass
                '''
                print str(Userinput)
                lookupmessage = "LOOKUP " + Userinput + " P2P-CI/1.0\nHost: " + str(myip)+ "\nPort: " + str(UploadPort) + "\nTitle: " + RFCTitle  + "\n"
                Peer.sendto(lookupmessage, (ServerIP,ServerPort))
                UDP_TupleList = Peer.recv(4096)
                print UDP_TupleList
                '''


class peer_upload(threading.Thread):
    def run(self):
        while True:
            #print Userinput
            try:
                print "\nready to listen in upload port ", UploadPort
                time.sleep(5)
                Request = Upload.recv(1024)
                print "Userinput received, ", repr(Request)
            except:
                print "except"
                return
            if Userinput == "disconnect":
                print "disconnect test"
                stopped = threading.Event()
                #set a timer, after 10 seconds.. kill this loop
                time.sleep(3)
                threading.Timer(1, stopped.set).start()
                return
            else:
                pass

            #RFCRequest = "Request " + Userinput;
            #Peer.sendto(RFCRequest, (UDP_IP, 8))



#UploadServer = socket(AF_INET,SOCK_STREAM)

#UploadServer.bind(("",UploadPort))
Peer = socket.socket(AF_INET,SOCK_STREAM);
Peer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

UploadPort = 7753;
Upload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Upload.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
Upload.bind(("",UploadPort))
print "The upload server is using port", UploadPort

#using my own pc as the server
ServerPort = 7734;
PeerPort = ServerPort+1;
myip = socket.gethostbyname(socket.gethostname())
ServerIP = myip;
print myip
Peer.connect((ServerIP,ServerPort)) # Connect
a=1;
Userinput = None;
#os.getcwd() #current directory when looking for files

RegistMessage = "REG This Computer " + "P2P-CI/1.0" +"\n"+"Host: " + str(myip) + "\n" +"Port: "+ str(UploadPort) + "\n"
Peer.sendto(RegistMessage, (ServerIP,ServerPort)) # Send request
print RegistMessage
RegACK=Peer.recv(4096)
print RegACK

for subdir, dirs, files in os.walk('./'):
    for file in files:
        if file.endswith(".txt"):
            name,ext = os.path.splitext(file)
            RFCnumber = name[3:]
            RFCTitle = " Some RFC title"
            filemessage = "ADD " + "RFC " + RFCnumber + " P2P-CI/1.0" + \
                      "\nHost: " + str(myip) + "\nPort: " + str(UploadPort) + "\nTitle: Some RFC number" + str(a)
            a += 1;
            Peer.sendto(filemessage, (ServerIP,ServerPort)) # Send request
            print filemessage
            Answer=Peer.recv(4096)
            print Answer
char = None;

talkwithserver = peer_send()
talkwithpeer = peer_upload()

talkwithserver.start()
talkwithpeer.start()
