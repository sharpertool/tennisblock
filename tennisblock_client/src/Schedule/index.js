import React from 'react'
import {render} from 'react-dom'

// Build the Store stuff
import mkStore from './modules'
import ScheduleProvider from './provider'
import './index.scss'

import { selectors, actions } from './modules'
export { selectors, actions }

const store = mkStore()

export default ({ target }) => {
  const onDateChanged = (currdate) => {
    console.log(`onDateChanged called with ${currdate}`)
    store.dispatch({
      type: 'UPDATE_CURRENT_DATE',
      payload: currdate
    })
    console.log('onDateChanged dispatched action')
  }

  const element = document.getElementById(target)

  render(
    <ScheduleProvider store={store}/>,
    element,
  )
  
  return onDateChanged
}