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
    [[  -1,'bp'], [5177,'dp'], [5178,'dp'], [5179,'dp']],
    [[5177,'dp'], [  -1,'bp'], [5180,'dp'], [5181,'dp']],
    [[5178,'dp'], [5180,'dp'], [  -1,'bp'], [5182,'dp']],
    [[5179,'dp'], [5181,'dp'], [5182,'dp'], [  -1,'bp']],
]
myIndex = -1       # Index of this bridge within the IPs list
myID = ''          # This bridge's ID is the MAC address
rootData = ['', 0] # [root bridge's ID, hops to root bridge's]
rootDataLock = threading.Lock()
portsLock = threading.Lock()

def getInfo():
  global myIndex
  global myID
  global rootData
  myIP = commands.getoutput("/sbin/ifconfig | grep -i \"inet\" | awk '{print $2}'")
  myIP = (myIP[5:13]).strip()
  myIndex = IPs.index(myIP)
  myMAC = commands.getoutput("/sbin/ifconfig | grep -i \"HWaddr\" | awk '{print $5}'")
  myID = myMAC
  rootData[0] = myID
  rootData[1] = 0

def createSocket():
  try: s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  except socket.error, errorMsg:
    print "Failed to crate socket: Error: ",errorMsg[0],": "+errorMsg[1]
    sys.exit(1)
  print "Socket Created"
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  return s

def sender():
  threading.Timer(3.0, sender).start()
  rootID = rootData[0]
  hopsToRoot = str(rootData[1])
  BDPU = rootID+' '+hopsToRoot+' '+myID
  # TODO remove
  print 'BDPU: ',BDPU 
  numPorts = len(ports[myIndex])
  for outPortIndex in range(0, numPorts):
    outPortNum = ports[myIndex][outPortIndex][0]
    outPortLabel = ports[myIndex][outPortIndex][1]
    if outPortNum != -1 and outPortLabel != 'bp':
      s = createSocket()
      try:
        outPortIP = IPs[outPortIndex]
        s.sendto(BDPU, (outPortIP, outPortNum))
        #print "Message sent successfully to ", outPortNum
      except socket.error:
        print "Send failed"
      s.close()
 
def listener(listenerID):
  global rootData
  global ports
  global rootDataLock
  global portsLock
  inPortNum = ports[myIndex][listenerID][0]
  myIP = IPs[myIndex]
  while(1):
    s = createSocket()
    s.bind((myIP, inPortNum))
    recvData = s.recv(4096)
    recvList = recvData.split()
    # TODO remove print
    #print 'list: ', recvList
    s.close()
    # Calculations
    recvRoot = recvList[0]
    recvHops = recvList[1]
    if recvRoot < rootData[0]:
      rootDataLock.acquire()
      rootData[0] = recvRoot
      rootData[1] = int(recvHops)+1
      rootDataLock.release()
      # set port label
      portsLock.acquire()
      ports[myIndex][listenerID][1] = 'rp'
      if imFurthestFromRoot():
        numPorts = len(ports[myIndex])
        for outPortIndex in range(0, numPorts):
          ports[myIndex][outPortIndex][1] = 'bp'
      portsLock.release()

def imFurthestFromRoot():
  # check if all listener-bound ports are marked 'rp'
  numPorts = len(ports[myIndex])
  for outPortIndex in range(0, numPorts):
    outPortNum = ports[myIndex][outPortIndex][0]
    outPortLabel = ports[myIndex][outPortIndex][1]
    if outPortNum != -1 and outPortLabel != 'rp':
      return false
  return true

if __name__ == '__main__':
  getInfo()
  s = createSocket() 
  # Create a listener thread for each of my incoming ports
  numPorts = len(ports[myIndex])
  for outPortIndex in range(0, numPorts):
    if ports[myIndex][outPortIndex][0] != -1:
      start_new_thread(listener, (outPortIndex,))
  # Create a sender thread
  start_new_thread(sender,()) 
  # Keep this process open or threads will die
  while(1):
    pass
