import unapply from 'ramda/src/unapply'
import mergeDeepRight from 'ramda/src/mergeDeepRight'
import reduce from 'ramda/src/reduce'

export const mergeDeepRightAll = unapply(reduce(mergeDeepRight, {}))
import axios from 'axios'
import MockAdapter from 'axios-mock-adapter'

import {applyMiddleware, createStore} from 'redux'
import {composeWithDevTools} from 'redux-devtools-extension'
import createSagaMiddleware from 'redux-saga'
import withReduxEnhancer from 'addon-redux/enhancer'
import createStorybookListener from 'storybook-addon-redux-listener'
import invariant from 'redux-immutable-state-invariant'
import {createLogger} from 'redux-logger'

import mkProvider from './provider'

/**
 *
 * @param  {object} historyType browserhistory, hashhistory, memory history
 * @param  {func} composer redux devtools composer or default composer
 * @param  {profile} profile
 * @return {[object]} created history, store, actions
 */
export const makeStore = (config, options = {}) => {
  const {rootSaga, rootReducer} = config

  const composeEnhancers = composeWithDevTools(options)

  const sagaMiddleware = createSagaMiddleware()

  const middlewares = [
    sagaMiddleware,
    invariant(),
    //createLogger(),
  ]

  // if (process.env.STORYBOOK === true) {
  //   const reduxListener = createStorybookListener()
  //   middlewares.push(reduxListener)
  //   console.log('Running under storybook environment, added redux listener')
  // } else {
  //   console.log('Sadly, the node environment is not storybook')
  // }

  const store = createStore(
    rootReducer,
    composeEnhancers(
      applyMiddleware(...middlewares),
      //withReduxEnhancer,
    )
  )

  sagaMiddleware.run(rootSaga, store.getState)

  return store
}

export const mockAxios = () => {
  const maxios = new MockAdapter(axios)

  maxios.onGet('/api/newsletter_status/').reply(
    200,
    {
      subscriber_status: {}
    })
  return maxios
}
