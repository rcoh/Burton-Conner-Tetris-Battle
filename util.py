from numpy import zeros
import socket
argDict = {'flags': 0, 'startcode': 0x0fff, 'pad':0}

# Allocate a buffer for transmitted packets and fill it with magic
# Only works for strips of 50 pixels
xmit = zeros(174, dtype='ubyte')
xmit[:8], xmit[20:25] = [4,1,220,74,1,0,8,1], [150,0,255,15,191]

def composePixelStripPacket(values, port):
  xmit[16], xmit[24:] = port, values.ravel()
  return xmit

def getConnectedSocket(ip,port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  try:
    sock.connect((ip, port))
    return sock
  except Exception as inst:
    print 'socket failure'
