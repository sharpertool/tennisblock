// This version requires lodash.. not sure if there is an advantage??
//import _ from 'lodash'

import unapply from 'ramda/src/unapply'
import mergeDeepRight from 'ramda/src/mergeDeepRight'
import reduce from 'ramda/src/reduce'

export const mergeDeepRightAll = unapply(reduce(mergeDeepRight, {}))

import DevTools from './DevTools'

export const phoneValidator = (value) => {
  const regex = /^(([+])?[0-9]{1,3}( |-))?(\(?[0-9]{3}\)?)( |-)?([0-9]{3}( |-)?[0-9]{4}|[a-zA-Z0-9]{7})$/g
  
  if (value) {
    return regex.test(value)
  }
  // this will allow for blank phone numbers
  // use Yup.required() to require not empty
  return true
}

import {applyMiddleware, compose, createStore} from 'redux'
import createSagaMiddleware from 'redux-saga'
import {createMiddleware as createBeaconMiddleware} from 'redux-beacon'

import GoogleTagManager from '@redux-beacon/google-tag-manager'

import commonEventsMap from './commonEventsMap'

// export const fromRoot = (path) =>
//   (selector) =>
//     (state, ...args) =>
//       selector(_.get(state, path), ...args);

// Version that does not require lodash
export const fromRoot2 = (path) =>
  (selector) =>
    (state, ...args) =>
      selector(state[path], ...args)

export const globalizeSelectors = (selectors, path) => {
  return Object.keys(selectors).reduce((final, key) => {
    final[key] = fromRoot2(path)(selectors[key])
    final[`${path}:${key}`] = fromRoot2(path)(selectors[key])
    return final
  }, {})
}

export const LocalDate = (date) => {
  const [yy, mm, dd] = date.split('-')
  return new Date(yy, mm-1, dd)
}

export const filter_keys = (props, prefix) => {
  // Require that the prefix is ':' separated
  if (!prefix.endsWith(':')) {
    prefix = prefix + ':'
  }
  const myprops = Object.keys(props)
    .filter(key => key.startsWith(prefix))
    .reduce((acc, key) => {
      // Remove the first : separated prefix only
      // This handles keys like prefix1:prefix2:...:keyvalue
      // And allows this same technique to be passed down to
      // lower level children, i.e. children of children
      const [_, ...k] = key.split(':')
      const partial_key = k.join(':')
      acc[partial_key] = props[key]
      return acc
    }, {})
  return myprops
}

export const prefix_keys = (obj, prefix) => {
  return Object.keys(obj)
    .reduce((acc, key) => {
      acc[`${prefix}:${key}`] = obj[key]
      return acc
    }, {})
}

/**
 *
 * @param  {object} historyType browserhistory, hashhistory, memory history
 * @param  {func} composer redux devtools composer or default composer
 * @param  {profile} profile
 * @return {[object]} created history, store, actions
 */
export const makeStore = (config) => {
  const {rootSaga, rootReducer, actions, options, eventsMap} = config
  
  const gtmEventsMap = mergeDeepRightAll(commonEventsMap, eventsMap)

  const sagaMiddleware = createSagaMiddleware()

  const gtm = GoogleTagManager()
  const beaconMiddleware = createBeaconMiddleware(gtmEventsMap, gtm)

  
  let middlewares = [
    beaconMiddleware,
    sagaMiddleware,
  ]
  
  const actionSanitizer = (action) => {
    return action
  }
  
  const composeEnhancers =
    typeof window === 'object' &&
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ ?
      window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__({
        // Specify extension’s options like name,
        //  actionsBlacklist, actionsCreators, serialize...
        actionSanitizer,
      }) : compose
  
  
  const enhancer = composeEnhancers(
    applyMiddleware(...middlewares),
  )
  
  const store = createStore(
    rootReducer,
    enhancer)
  
  sagaMiddleware.run(rootSaga, store.getState)
  
  return store
}

export const connect_site_actions = ({store, actions}) => {
  
}
