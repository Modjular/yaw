function startWebSocket() {

  const socket = new WebSocket(`wss://${window.location.host}/deviceorientation`)
  socket.onopen = () => console.log('WebSocket connection opened')
  socket.onclose = () => console.log('WebSocket connection closed')

  window.addEventListener('deviceorientation', (event) => {
    var roll = event.gamma // Roll: Left to Right
    var pitch = event.beta // Pitch: Front to Back
    var yaw = event.alpha // Yaw: Compass

    // Display the data
    document.getElementById('roll').textContent = roll.toFixed(2)
    document.getElementById('pitch').textContent = pitch.toFixed(2)
    document.getElementById('yaw').textContent = yaw.toFixed(2)

    const data = {
      roll,
      pitch,
      yaw,
    }

    if (socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(data))
    }
  })
}


// Request permission on load
window.onload = function() {
  if (typeof DeviceOrientationEvent !== 'undefined' && typeof DeviceOrientationEvent.requestPermission === 'function') {
    // iOS 13+ requires user permission
    DeviceOrientationEvent.requestPermission()
    .then(response => {
        if (response === 'granted') {
            startWebSocket()
        }
    })
    .catch(console.error);
} else {
    // Non-iOS 13+ devices
    startWebSocket()
}}

