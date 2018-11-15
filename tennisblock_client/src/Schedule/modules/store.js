import createSagaMiddleware from 'redux-saga'
import {createStore, compose, applyMiddleware} from 'redux'
import {combineReducers} from 'redux'

import rootSaga from './sagas'

// Default from each 'Duck' module is the reducer
import schedule_reducer, {MODULE_NAME as schedule_name} from './schedule'
import teams_reducer, {MODULE_NAME as teams_name} from './teams'

const rootReducer = combineReducers({
  [schedule_name]: schedule_reducer,
  [teams_name]: teams_reducer,
})

const sagaMiddleware = createSagaMiddleware()

let middlewares = [
  sagaMiddleware
]

let composeStore = compose(
  applyMiddleware(...middlewares),
)(createStore)

const store = composeStore(
  rootReducer,
  window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__()
)

sagaMiddleware.run(rootSaga, store.getState)

export {rootReducer}

export default store






