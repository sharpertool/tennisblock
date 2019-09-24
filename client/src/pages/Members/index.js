import React from 'react'
import {render} from 'react-dom'


export const moduleConfig = {
  axios_config: {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
  },
}

import {selectors, actions, eventsMap, rootSaga, rootReducer, set_config, initialize} from './modules'

export {selectors, actions}
import {makeStore, connect_site_actions} from '~/utils'

import Root from './root'

export default (elements, options) => {
  const {members_el} = elements
  
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
    <Root store={store}/>
    , document.getElementById(members_el)
  )
}
