import React from 'react'
import {render} from 'react-dom'

import './index.scss'

export const moduleConfig = {
  axios_config: {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
  },
}

import {selectors, actions, eventsMap, rootSaga, rootReducer, set_config, initialize} from './modules'
export {selectors, actions }
import {makeStore, connect_site_actions} from '~/utils'

import Root from './root'

export default (elements, options) => {
  const { schedule_el } = elements

  moduleConfig.selectors = selectors

  set_config({defaults: moduleConfig, options: options})

  // Create the store
  const store = makeStore({
    rootSaga: rootSaga,
    rootReducer: rootReducer,
    actions: actions,
    options: options,
    eventsMap: eventsMap,
  })

  connect_site_actions({
    store: store, actions: actions
  })

  initialize(options)

  render(
    <Root store={store}/>,
    document.getElementById(schedule_el)
  )
}


const old_code =  ({ target }) => {
  const onDateChanged = (currdate) => {
    console.log(`onDateChanged called with ${currdate}`)
    store.dispatch({
      type: 'UPDATE_CURRENT_DATE',
      payload: currdate
    })
    console.log('onDateChanged dispatched action')
  }

  return onDateChanged
}