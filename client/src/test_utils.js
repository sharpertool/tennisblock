import React from 'react'
import {createStore, applyMiddleware, compose} from 'redux'
import createSagaMiddleware from 'redux-saga'
import {Provider} from 'react-redux'
import {render} from '@testing-library/react'

// Import the "All Reducers" testing version as default
import {rootReducer, set_config} from '~/pages/StoriesTestingPage/modules'
import {selectors, actions} from './pages/StoriesTestingPage'

/**
 * Create a renderer that wraps the store, for use in testing.
 * @param reducer
 * @param configState
 * @returns {function(*, *=): ({container: HTMLElement; baseElement: HTMLElement; debug: (baseElement?: (HTMLElement | DocumentFragment)) => void; rerender: (ui: React.ReactElement<any>) => void; unmount: () => boolean; asFragment: () => DocumentFragment}&{[P in keyof Q]: BoundFunction<Q[P]>}&{store: *})}
 */
export const createRenderer = ({
                                 reducer = rootReducer,
                                 configState = {},
                                 rootSaga = null,
                               }) => {
  return (
    ui,
    overrideState = {}) => {
    
    const initialState = {...configState, ...overrideState}
    
    const sagaMiddleware = createSagaMiddleware()
    
    const middlewares = [
      sagaMiddleware
    ]
    
    const moduleConfig = {
      selectors: selectors,
      actions: actions,
    }
    
    set_config({defaults: moduleConfig, options: {}})
    
    const store = createStore(
      reducer,
      initialState,
      compose(
        applyMiddleware(...middlewares),
      )
    )
    
    // We do not want to run the root saga on the entire state tree
    // As that will try an run all initial sagas... not desireable for testing
    // If you need to run a set of sagas for a particular module, then pass
    // that in here. By default, no sagas run
    if (rootSaga) {
      sagaMiddleware.run(rootSaga, store.getState)
    }
    
    return {
      ...render(<Provider store={store}>{ui}</Provider>),
      // adding `store` to the returned utilities to allow us
      // to reference it in our tests (just try to avoid using
      // this to test implementation details).
      store,
    }
    
  }
}
