# Protocol.py
import socket
import sys
from thread import *
import threading
import time
import commands

# Tables are used by maping row and column to Node id number - 1
IPs= ['10.0.0.1','10.0.0.2','10.0.0.3','10.0.0.4']
ports = [
    [[  -1,'dp'], [5177,'dp'], [5178,'dp'], [5179,'dp']],
    [[5177,'dp'], [  -1,'dp'], [5180,'dp'], [5181,'dp']],
    [[5178,'dp'], [5180,'dp'], [  -1,'dp'], [5182,'dp']],
    [[5179,'dp'], [5181,'dp'], [5182,'dp'], [  -1,'dp']],
]
myIndex = -1
myID = ''
rootData = ['', 0]

def getInfo():
  global myIndex
  global myID
  global root
  myIP = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | awk '{print $2}'")
  myIP = (myIP[5:13]).strip()
  myIndex = IPs.index(myIP)
  myMAC = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
  root = myID

def createSocket():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1.0)
  except socket.error, errorMsg:
    print "Failed to crate socket: Error: ",errorMsg[0],": "+errorMsg[1]
    sys.exit(1)
  print "Socket Created"
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  return s

def sender():
  while (1):
    for i in range(0, len(ports[myIndex])):
      if ports[myIndex][i][0] != -1:
        s = createSocket()
        try:
          BDPU = rootData[0]+' '+rootData[1]+' '+ myID
          s.sendto(ports[myThread]
          s.close()
          threading.timer(5, sender)
        except socket.error:
        print "Send failed"
      print "Message sent successfully to ", ports[myThread][i][0]
  
  # Receive message from host
  reply = s.recv(4096)
  print reply

def listener(listenerID):
  s = createSocket()
  server_socket.bind((IPs[myIndex], ports[myIndex][listenerID])
  

if __name__ == '__main__':
  getInfo()
  s = createSocket()
   
  # Create a listener thread for each of my links
  for i in range(0, len(ports[myIndex])):
    start_new_thread(listener, (i,))

  # Create a sender thread
  start_new_thread(sender,())
  #print "Socket connected to \n",host,"\non ip ",remote_ip,"\nthrough port ",port
  
    
  # Keep this thread open for data access
  #while(!error):
  #s.close()

