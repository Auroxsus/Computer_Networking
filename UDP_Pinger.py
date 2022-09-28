#   Send 10 ping messages through UDP
#   Format of message: 'Ping ping#_pingTime

from socket import *
from time import *

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1.0)

pingNumber = 0
startTime = time()

while pingNumber < 10:
    pingNumber = pingNumber + 1
    pingTime = time()-startTime
    message = "Ping {} {:.5f}".format(pingNumber, pingTime)
    clientSocket.sendto(message.encode(), ("127.0.0.1", 12000))
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode() + "\n\tRTT = {:.8f} ms".format((time()-startTime-pingTime)*1000))
    except timeout:
        print("Request timed out")
clientSocket.close()
