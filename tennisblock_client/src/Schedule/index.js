import React from 'react'
import {render} from 'react-dom'
import {Provider} from 'react-redux'

import './index.scss'

// Build the Store stuff
import makeStore from 'Schedule/modules'

import Root from './root'

export default (element) => {
  const store = makeStore(null, null);
  console.log(`Mounting at ${element}`)
  render(<Root store={store}/>, document.getElementById(element))
  console.log('Schedule React component mounted')
}