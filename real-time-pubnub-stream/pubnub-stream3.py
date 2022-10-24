# This code is a Python3 port of https://gist.github.com/stephenlb/9496723#file-publish-lots-of-pubnub-messages-py

import socket
import uuid
import random
import threading
import time
import random
import math

HOST = 'pubsub.pubnub.com'
PORT = 80

numID = random.randrange(5000, 10000)
print ('creating', numID, ' UUIDs')

id = []
for x in range(0, numID-1):
    id.append(uuid.uuid4())

print ('We will send a random quantity of messages every 10 seconds, each contains a randomly selected UUID.')

def handleSocketRead(s):
    while True:
        try:
            msg = s.recv(4096)
        except (socket.timeout):
            print ('recv timed out, done reading')
            break
        except (socket.error, e):
            print (e)
            break
        else:
            continue

def send():
    time.sleep(10)
    threading.Thread(target=send).start()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostbyname(HOST), PORT))
    s.settimeout(2)
    numMessages = random.randrange(math.floor(0.5*numID), 2*numID)
    print ('Sending '+ str(numMessages) +' messages.')
    time_start = time.time()
    tmr = threading.Thread(target=handleSocketRead, args=[s])
    tmr.start()
    for message in range(0, numMessages):
        #print ('we are on message', message+1, 'of', numMessages)
        temp_str = 'GET /publish/YOUR_PUBLISH_KEY/YOUR_SUBSCRIBE_KEY/0/streamtest/0/"'+str(id[random.randrange(0, numID-1)])+'" HTTP/1.1\r\nHost: pubsub.pubnub.com\r\n\r\n'
        s.send(temp_str.encode())
    print ('It took', str(time.time()-time_start), 'runtime to send', numMessages, 'messages')
    handleSocketRead(s)
    s.close()

send()