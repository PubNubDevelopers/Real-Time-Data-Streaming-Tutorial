// Replaces addFormattedMessageWikipedia in js/index.js of
// https://github.com/PubNubDevelopers/Real-Time-Data-Streaming-Demo
// so the demo shows the raw Wikimedia events that real-time-pubnub-sdk/index.js publishes.
function addFormattedMessageWikipedia (payload) {
  var li = document.createElement('li')
  li.setAttribute('class', 'list-group-item')
  var fields = [
    ['Source', 'Wikimedia (' + payload.message.server_name + ')'],
    ['Title', payload.message.title],
    ['User', payload.message.user],
    ['Timestamp', new Date(payload.timetoken / 10000)]
  ]
  fields.forEach(function (field) {
    var label = document.createElement('b')
    label.textContent = field[0] + ': '
    li.appendChild(label)
    li.appendChild(document.createTextNode(field[1]))
    li.appendChild(document.createElement('br'))
  })
  var list = document.getElementById('messageList')
  list.insertBefore(li, list.firstChild)
  capElements()
}
