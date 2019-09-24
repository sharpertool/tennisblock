import clone from 'ramda/src/clone'
import {mergeDeepRightAll} from '~/modules/module_utils'
import * as types from './constants'

let configInitialState = {
  blockmembers: [],
}

export const update_initial_state = (initial_state) => {
  configInitialState = mergeDeepRightAll(configInitialState, initial_state)
}


function reducer(state = clone(configInitialState), action) {
  switch(action.type) {
    case types.UPDATE_BLOCK_MEMBERS: {
      return {
        ...state,
        blockmembers: action.payload
      }
    }
    default: return state
  }
}

export default reducer
