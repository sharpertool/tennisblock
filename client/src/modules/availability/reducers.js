import clone from 'ramda/src/clone'
import {mergeDeepRightAll} from '~/modules/module_utils'
import * as R from 'ramda'
import { handleActions } from 'redux-actions'
import * as types from './constants'
import {
  groupByGenderAndId,
  toObjectById
} from './ramda_utils'

let configInitialState = {
  availability: [],
}

export const update_initial_state = (initial_state) => {
  configInitialState = mergeDeepRightAll(configInitialState, initial_state)
}


function reducer(state = clone(configInitialState), action) {
  switch(action.type) {
    case types.UPDATE_AVAILABILITY: {
      return {
        ...state,
        availability: action.payload,
      }
    }
    case types.UPDATE_PLAYER_AVAILABILITY: {
      // ToDo: Update the player by ID
      // Payload: {id: nn, mtgidx: nn, isavail: true|false}
      return {
        ...state,
      }
    }
    default: return state
  }
}

export default reducer
