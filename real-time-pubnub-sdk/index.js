const EventSource = require('eventsource')
const PubNub = require('pubnub')

const url = 'https://stream.wikimedia.org/v2/stream/recentchange'
const eventSource = new EventSource(url)
var last_message = null

var wikipedia_pubnub = new PubNub({
  publish_key: 'YOUR_PUBLISH_KEY',
  subscribe_key: 'YOUR_SUBSCRIBE_KEY',
  userId: 'real-time-tutorial'
})

eventSource.onmessage = async event => {
  const data = JSON.parse(event.data)
  //if (data.server_name === 'en.wikipedia.org') {
    console.log(data)
    try {
      const result = await wikipedia_pubnub.publish({
        channel: "pubnub-wikipedia",
        message: data
      })
    } catch (e) {}
  //}
}
