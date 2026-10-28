# This code is a Python 3 port of https://gist.github.com/stephenlb/9496723#file-publish-lots-of-pubnub-messages-py

import socket
import ssl
import uuid
import random
import threading
import time
import math
from urllib.parse import quote

PUBLISH_KEY = 'YOUR_PUBLISH_KEY'
SUBSCRIBE_KEY = 'YOUR_SUBSCRIBE_KEY'
CHANNEL = 'streamtest'
USER_ID = 'stream-tutorial'

HOST = 'ps.pndsn.com'
PORT = 443

numID = random.randrange(5000, 10000)
print('creating', numID, 'UUIDs')

id = []
for x in range(0, numID-1):
    id.append(uuid.uuid4())

print('We will send a random quantity of messages every 10 seconds, each contains a randomly selected UUID.')

context = ssl.create_default_context()

def handleSocketRead(s, numMessages):
    # Each accepted publish returns [1,"Sent","<timetoken>"]. Count them until all have arrived.
    accepted = 0
    tail = b''
    while accepted < numMessages:
        try:
            msg = s.recv(65536)
        except socket.timeout:
            print('recv timed out, done reading')
            break
        except socket.error as e:
            print(e)
            break
        if not msg:
            break
        chunk = tail + msg
        accepted += chunk.count(b'[1,"Sent"')
        tail = chunk[-8:]  # A reply split across two reads is counted once it's complete.
    print('PubNub accepted', accepted, 'of', numMessages, 'messages')

def send():
    time.sleep(10)
    threading.Thread(target=send).start()
    s = context.wrap_socket(socket.create_connection((HOST, PORT)), server_hostname=HOST)
    s.settimeout(10)
    numMessages = random.randrange(math.floor(0.5*numID), 2*numID)
    print('Sending ' + str(numMessages) + ' messages.')
    time_start = time.time()
    tmr = threading.Thread(target=handleSocketRead, args=[s, numMessages])
    tmr.start()
    for message in range(0, numMessages):
        payload = quote('"' + str(id[random.randrange(0, numID-1)]) + '"')
        path = '/publish/' + PUBLISH_KEY + '/' + SUBSCRIBE_KEY + '/0/' + CHANNEL + '/0/' + payload + '?uuid=' + USER_ID
        s.sendall(('GET ' + path + ' HTTP/1.1\r\nHost: ' + HOST + '\r\n\r\n').encode())
    print('It took', str(time.time()-time_start), 'seconds to send', numMessages, 'messages')
    tmr.join()
    s.close()

send()
