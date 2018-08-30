import rootSaga from '~/ImageEditor/sagas'
import modules from '~/ImageEditor/modules'
import createSagaMiddleware from 'redux-saga'
import { createStore, compose, applyMiddleware } from 'redux'
import { bindActionCreatorsToStore } from 'redux-module-builder'

const {
    reducers,
    actions,
    initialState
} = modules()

const sagaMiddleware = createSagaMiddleware()

let middlewares = [
    sagaMiddleware
]

const creator = (composer) => {
  if(composer) return composer
  return compose
}

/**
 *
 * @param  {object} historyType browserhistory, hashhistory, memory history
 * @param  {func} composer redux devtools composer or default composer
 * @return {[object]} created history, store, actions
 */
export default (historyType, composer) => {
    const create = creator(composer)

    let composeStore = create(
        applyMiddleware(...middlewares),
    )(createStore)

    const store = composeStore(reducers, initialState)

    sagaMiddleware.run(rootSaga, store.getState)

    return {
        history: null,
        store,
        actions: bindActionCreatorsToStore(actions, store),
    }
}
