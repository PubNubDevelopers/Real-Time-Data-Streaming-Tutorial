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
BATCH = 1000  # Publish requests in flight on the connection at once

numID = random.randrange(5000, 10000)
print('creating', numID, 'UUIDs')

id = []
for x in range(0, numID-1):
    id.append(uuid.uuid4())

print('We will send a random quantity of messages every 10 seconds, each contains a randomly selected UUID.')

context = ssl.create_default_context()

def readReplies(s, numReplies):
    # Each publish gets one reply: [1,"Sent","<timetoken>"] if PubNub accepted it,
    # or [0,"<reason>",...] if it rejected it. Count both until all have arrived.
    accepted = rejected = 0
    reason = None
    tail = b''
    while accepted + rejected < numReplies:
        try:
            msg = s.recv(65536)
        except socket.timeout:
            print('recv timed out, done reading')
            break
        if not msg:
            print('PubNub closed the connection')
            break
        chunk = tail + msg
        accepted += chunk.count(b'[1,"')
        rejected += chunk.count(b'[0,"')
        if rejected and reason is None and b'[0,"' in chunk:
            reason = chunk[chunk.index(b'[0,"') + 4:].split(b'"')[0].decode(errors='replace')
        tail = chunk[-3:]  # Both markers are 4 bytes, so a marker split across two reads is counted once.
    return accepted, rejected, reason

def request():
    payload = quote('"' + str(id[random.randrange(0, numID-1)]) + '"')
    path = '/publish/' + PUBLISH_KEY + '/' + SUBSCRIBE_KEY + '/0/' + CHANNEL + '/0/' + payload + '?uuid=' + USER_ID
    return 'GET ' + path + ' HTTP/1.1\r\nHost: ' + HOST + '\r\n\r\n'

def send():
    time.sleep(10)
    threading.Thread(target=send).start()
    numMessages = random.randrange(math.floor(0.5*numID), 2*numID)
    print('Sending ' + str(numMessages) + ' messages.')
    time_start = time.time()
    accepted = 0
    try:
        s = context.wrap_socket(socket.create_connection((HOST, PORT), timeout=10), server_hostname=HOST)
    except OSError as e:
        print('Could not connect to', HOST + ':', e)
        return
    try:
        # Pipelining: write BATCH requests in one go without waiting, then read their replies.
        # One thread does both, because a TLS socket can't be read and written from two threads at once.
        for start in range(0, numMessages, BATCH):
            count = min(BATCH, numMessages - start)
            s.sendall(''.join(request() for _ in range(count)).encode())
            ok, rejected, reason = readReplies(s, count)
            accepted += ok
            if rejected:
                print('PubNub rejected', rejected, 'messages:', reason)
                break
            if ok < count:
                break
    except OSError as e:
        print('Connection error:', e)
    finally:
        s.close()
    print('It took', str(time.time()-time_start), 'seconds to send', numMessages, 'messages')
    print('PubNub accepted', accepted, 'of', numMessages, 'messages')

send()
