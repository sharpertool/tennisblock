import clone from 'ramda/src/clone'
import {mergeDeepRightAll} from '~/modules/module_utils'

import * as types from './constants'

let configInitialState = {
  guys: [],
  girls: [],
  couples: [],
}

export const update_initial_state = (initial_state) => {
  configInitialState = mergeDeepRightAll(configInitialState, initial_state)
}

function mainReducer(state = clone(configInitialState), action) {
  switch (action.type) {
    case types.UPDATE_PLAYERS: {
      const {guys, girls} = action.payload
      return {...state, guys: guys, girls: girls}
    }
    default:
      return state
  }
}

export default mainReducer
