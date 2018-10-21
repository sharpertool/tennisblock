import createSagaMiddleware from 'redux-saga'
import {createStore, compose, applyMiddleware} from 'redux'
import {combineReducers} from 'redux'

import rootSaga from './sagas'

// Default from each 'Duck' module is the reducer
import schedule_reducer, {NAME as schedule_name} from './schedule'
import teams_reducer, {NAME as teams_name} from './teams'

const rootReducer = combineReducers({
  [schedule_name]: schedule_reducer,
  [teams_name]: teams_reducer,
})

const sagaMiddleware = createSagaMiddleware()

let middlewares = [
  sagaMiddleware
]


/**
 *
 * @param  {object} historyType browserhistory, hashhistory, memory history
 * @param  {func} composer redux devtools composer or default composer
 * @param  {profile} profile
 * @return {[object]} created history, store, actions
 */
export default (historyType, composer) => {
  const _compose = (composer) => composer || compose

  let composeStore = _compose(composer)(
    applyMiddleware(...middlewares),
  )(createStore)

  const store = composeStore(
    rootReducer,
    window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
  )

  sagaMiddleware.run(rootSaga, store.getState)

  return store
}

export {rootReducer}

