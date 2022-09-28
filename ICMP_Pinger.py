from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8

def pingStats(dest):
    print("\nPing statistics of", gethostbyname(dest))
    print("{:<31} {:<10}{:<14} {:<10}{:<1}%".format("packets transmitted:10", "packets received:", roundTrip_cnt,
                                                    "packet loss:", 100.0 - roundTrip_cnt * 100.0 / 10))
    print("trip min:", roundTrip_min, "\ttrip avg:", roundTrip_sum / roundTrip_cnt, "\ttrip max:", roundTrip_max)


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        Values = string[count + 1] * 256 + string[count]
        csum = csum + Values
        csum = csum & 0xffffffff
        count = count + 2

    if countTo < len(string):
        csum = csum + string[len(string) - 1]  
        csum = csum & 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    # Variables to calculate the round-trip time for each packet
    global roundTrip_min, roundTrip_max, roundTrip_sum, roundTrip_cnt

    timeLeft = timeout

    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return "0: Destination Network Unreachable"  # Optional ICMP response error code

        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)

        # Fetch the ICMP header from the IP packet
        icmpHeader = recPacket[20:28]
        requestType, code, revChecksum, revId, revSequence = struct.unpack('bbHHh', icmpHeader)
        if revId == ID: 
            bytesInDouble = struct.calcsize('d')
            timeData = struct.unpack('d', recPacket[28:28 + bytesInDouble])[0]
            '''# ping stats
            print('requestType {}, code {}, revChecksum {}, revId {}, revSequence {}, TTL {}'.format(requestType, code,
                revChecksum, revId, revSequence, icmpHeader[5]))
            '''
            roundTrip = (timeReceived - timeData) * 1000
            roundTrip_cnt = roundTrip_cnt + 1
            roundTrip_sum += roundTrip
            roundTrip_min = min(roundTrip_min, roundTrip)
            roundTrip_max = max(roundTrip_max, roundTrip)

            return timeReceived - timeData  # RTT - round trip time

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "1: Destination Host Unreachable."  # Optional ICMP response error code


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)

    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # Struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())

    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)  # checksum(str(header + data))

    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details: http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay


# timeout=1 means: If one second goes by without a reply from the server,
# The client assumes that either the client's ping or the server's pong is lost
def ping(host, timeout=1):
    # Variables to calculate the round-trip time for each packet
    global roundTrip_min, roundTrip_max, roundTrip_sum, roundTrip_cnt

    dest = gethostbyname(host)
    print("\nPinging " + dest + " using Python:")
    print("")

    # Initialize variables for every ping call
    roundTrip_min = float('+inf')
    roundTrip_max = float('-inf')
    roundTrip_sum = 0
    roundTrip_cnt = 0

    # Send ping requests to a server separated by approximately one second
    count = 0  # limits how many times it pings
    while count < 10:  # changed from while 1:
        count = count + 1
        delay = doOnePing(dest, timeout)
        print("RTT:", delay)
        time.sleep(1)  # one second
    return delay

#ping("google.com")  # north america - usa
#pingStats("google.com")
#ping("google.co.jp")  # asia - japan
#pingStats("google.co.jp")
#ping("google.es")  # europe - spain
#pingStats("google.es")
ping("google.com.au")  # oceania - australia
pingStats("google.com.au")
