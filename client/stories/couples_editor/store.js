import {createStore, compose, applyMiddleware} from 'redux'
import createSagaMiddleware from 'redux-saga'

import {selectors, actions, rootSaga, rootReducer, set_config, initialize} from '~/pages/StoriesTestingPage/modules'
export {selectors, actions }
import {makeStore, connect_site_actions} from '~/utils'

/**
 *
 * @param  {object} historyType browserhistory, hashhistory, memory history
 * @param  {func} composer redux devtools composer or default composer
 * @param  {profile} profile
 * @return {[object]} created history, store, actions
 */
export default (composer = {}) => {
  const _compose = (composer) => composer || compose
  
  const sagaMiddleware = createSagaMiddleware()
  
  let middlewares = [
    sagaMiddleware
  ]
  
  let composeStore = _compose(composer)(
    applyMiddleware(...middlewares)
  )(createStore)
  
  const store = composeStore(
    rootReducer,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
  )
  
  sagaMiddleware.run(rootSaga)
  
  return store
}

