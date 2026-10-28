const { EventSource } = require('eventsource')
const PubNub = require('pubnub')

const url = 'https://stream.wikimedia.org/v2/stream/recentchange'
const eventSource = new EventSource(url)

const pubnub = new PubNub({
  publishKey: 'YOUR_PUBLISH_KEY',
  subscribeKey: 'YOUR_SUBSCRIBE_KEY',
  userId: 'real-time-tutorial'
})

eventSource.onmessage = async event => {
  try {
    const data = JSON.parse(event.data)
    // To publish changes from one wiki only, wrap the rest in: if (data.server_name === 'en.wikipedia.org') { ... }
    console.log(data.server_name, data.type, data.title)
    await pubnub.publish({
      channel: 'pubnub-wikipedia',
      message: data
    })
  } catch (e) {
    console.error('Publish failed:', e.message, e.status?.errorData ?? '')
  }
}

eventSource.onerror = error => {
  console.error('Wikimedia stream error:', error.message ?? error)
}
