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
  blockdates: [],
  scrollLeft: 0,
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
      const {id, mtgidx, isavail} = action.payload
      const newav = state.availability.map((item, idx) => {
        if (item.id != id) {
          return item
        }
        // This is our item to update
        const newavail = item.isavail.slice()
        newavail[mtgidx] = isavail
        return {
          ...item,
          isavail: newavail
        }
      })
      return {
        ...state,
        availability: newav
      }
    }
    case types.UPDATE_BLOCK_DATES: {
      return {
        ...state,
        blockdates: action.payload
      }
    }
    case types.ON_ITEMS_SCROLL:
      return {...state, scrollLeft: action.payload}
    default: return state
  }
}

export default reducer
