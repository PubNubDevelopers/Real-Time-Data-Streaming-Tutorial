# Tutorial: Real-Time Data Streaming with PubNub

**PubNub makes it easy to connect and consume large amounts of real-time streaming data, and deliver it to any number of subscribers.** These "firehoses of data" could be weather reports, business metrics, stock quotes or sensor readings: any source of data that is constantly changing and emitting updates.

## Tutorial

This repository accompanies the [real-time data streaming tutorial](https://www.pubnub.com/tutorials/real-time-data-streaming/). It has two parts:

- `real-time-pubnub-sdk/`: a Node.js app that reads Wikimedia's [recent changes stream](https://stream.wikimedia.org/?doc#/streams/get_v2_stream_recentchange) and [publishes](https://www.pubnub.com/docs/pub-sub/publish/overview) every change to PubNub with the [JavaScript SDK](https://www.pubnub.com/docs/sdks/javascript).
- `real-time-pubnub-stream/`: a Python 3 script that sends thousands of messages over one connection with HTTP pipelining, and a URL to watch them with HTTP streaming.

![Screenshot](https://raw.githubusercontent.com/PubNubDevelopers/Real-Time-Data-Streaming-Tutorial/main/media/stream1.gif)

Tested with the PubNub JavaScript SDK 13.1.3, Node.js 24 and Python 3.15 (October 2026).

## Running

You need [Node.js](https://nodejs.org/en/download) 22 or later, [Python 3](https://www.python.org/downloads/) and your own PubNub publish and subscribe keys from the [Admin Portal](https://admin.pubnub.com/).

```
git clone https://github.com/PubNubDevelopers/Real-Time-Data-Streaming-Tutorial.git
cd Real-Time-Data-Streaming-Tutorial
```

Publish Wikimedia changes with the SDK: replace `YOUR_PUBLISH_KEY` and `YOUR_SUBSCRIBE_KEY` in `real-time-pubnub-sdk/index.js`, then:

```
cd real-time-pubnub-sdk
npm install
npm start
```

Stream with HTTP pipelining: replace the same placeholders in `real-time-pubnub-stream/pubnub-stream3.py`, then:

```
python3 real-time-pubnub-stream/pubnub-stream3.py
```

Follow the [tutorial](https://www.pubnub.com/tutorials/real-time-data-streaming/) for how to watch the messages arrive.

## Contributing

Please fork the repository if you'd like to contribute. Pull requests are always welcome.

## Links

- Data streaming demo: https://www.pubnub.com/demos/real-time-data-streaming/
- Data streaming solutions: https://www.pubnub.com/solutions/data-streaming/
- JavaScript SDK documentation: https://www.pubnub.com/docs/sdks/javascript

