import {END, eventChannel} from '@redux-saga/core'
import {captureEvent, captureException, captureMessage} from '@sentry/minimal'
import {call, cancelled, delay, put, take} from '@redux-saga/core/effects'

export function setupChannelsEvent(socket, options={}) {
  
  return eventChannel(emitter => {
    
    socket.onopen = () => {
      if (options.onconnect_send) {
        socket.send(JSON.stringify(options.onconnect_send))
      }
    }
    
    socket.onerror = (error) => {
      captureMessage(`Websocket error ${error}`)
    }
    
    socket.onclose = function(e) {
      emitter(END)
    }
    
    socket.onmessage = function(e) {
      return emitter(e.data)
    }
    
    return () => {
      socket.close()
    }
    
  })
}

export function* watchInternal(channel, actions) {
  try {
    while (true) {
      const packet = yield take(channel)
      try {
        const data = JSON.parse(packet)
        let {action, payload} = data
        
        try {
          payload = JSON.parse(payload)
        } catch (e) {
          // Not json, payload is left untouched
        }
        
        if (action in actions) {
          yield put(actions[action](payload))
        } else {
          captureEvent({
            message: 'Invalid action from websockets',
            extra: {
              action: action,
            }
          })
        }
      } catch (e) {
        captureException(e)
      }
    }
  } finally {
    if (yield cancelled()) {
      channel.close()
    }
  }
}

/**
 * connectionManager
 *
 * Generator that will create a websocket connection,
 * setup a eventChannel to receive messages, and reconnect
 * if the connection is closed for any reason.
 * @returns {IterableIterator<CallEffect|IterableIterator<*>>}
 */
export function* connectionManager(url, actions, options={}) {
  
  // Delay 4 to 8 seconds
  // Actual value is random for each client.
  const delayMin = 4
  const delayMax = 8
  
  // Calculate ws or wss and path
  const loc = window.location;
  let full_url = 'ws:'
  if (loc.protocol === 'https:') {
      full_url = 'wss:';
  }
  full_url += '//' + loc.host;
  full_url += url.charAt(0) == '/' ? url : '/'+url;
  
  let onconnect_send = null
  if (options.onconnect_send) {
    onconnect_send = options.onconnect_send
  }
  
  while (true) {
    try {
      const socket = new WebSocket(full_url)
      let channel = yield call(setupChannelsEvent, socket, options)
      
      yield watchInternal(channel, actions)
    } catch (e) {
      // If the server is down, this can happen. We will fall out to
      // the retries, and attempt a new connection hopefully.
      captureException(e)
    }
    
    // At this point our channel has disconnected
    // Wait for a random delay in a fixed range,
    // then retry the connection.
    const dval = Math.floor(
      1000 * (
        delayMin + Math.random() * (delayMax - delayMin)
      )
    )
    yield delay(dval)
  }
}

