import React from 'react'
import '@testing-library/jest-dom/extend-expect'
import 'sinon'
import {
  render,
  fireEvent,
  cleanup,
  waitForElement,
  waitForElementToBeRemoved,
} from '@testing-library/react'
// Store stuff
import {createStore} from 'redux'
import {Provider} from 'react-redux'
import '@testing-library/jest-dom/extend-expect'
import {rootReducer} from '~/pages/Schedule/modules'

const initialState = {}

import ErrorBoundary from '~/components/errorboundary/error_boundary'

// this is a handy function that I normally make available for all my tests
// that deal with connected components.
// you can provide initialState for the entire store that the ui is rendered with
function renderWithRedux(
  ui,
  {initialState, store = createStore(rootReducer, initialState)} = {account: {}}
) {
  //console.log('Store', store.getState())
  return {
    ...render(
      <Provider store={store}>
        <ErrorBoundary>
          {ui}
        </ErrorBoundary>
      </Provider>),
    // adding `store` to the returned utilities to allow us
    // to reference it in our tests (just try to avoid using
    // this to test implementation details).
    store,
  }
}

import {configInitialState} from '~/modules/schedule/reducers'
import {selectors} from '~/pages/Schedule/modules'

describe('Schedule selectors', () => {

  const players = [
    {id: 20, name: 'Ed'},
    {id: 6, name: 'Jake'},
    {id: 30, name: 'Bob'},
    {id: 31, name: 'Kitty'},
    {id: 32, name: 'Randy'},
    {id: 33, name: 'Kris'},
    {id: 40, name: 'Jack'},
    {id: 41, name: 'Ted'},
    {id: 42, name: 'Fred'},
    {id: 43, name: 'Anne'},
    {id: 44, name: 'Kathy'},
    {id: 45, name: 'Ellen'},
  ]
  const subs = []

  const byid = players.reduce((acc, p) => {
    acc[p.id] = p
    return acc
  }, {})

  const setup = () => {
    const store = createStore(rootReducer, {
      schedule: {
        ...configInitialState,
        players_by_id: byid,
        curr_guys: [20, 6, 30, 32],
        curr_gals: [33, 43, 45, 44],
        num_courts: 4,
        couples: [[20, 33], [6,43], [30,45], [32,44]]
      }
    })
    const state = store.getState()
    console.log(state)
    return state
  }

  it('It returns some value', () => {
    const state = setup()
    const couples = selectors.couples(state)


    expect(couples).toEqual(state.schedule.couples)
  })

  it('Should return advanced couples', () => {
    const state = setup()
    const couples = selectors.getCouples(state)
    const couples2 = selectors.getCouples2(state)

    expect(couples2).toEqual(couples)

  })
})
