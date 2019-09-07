import clone from 'ramda/src/clone'
import {mergeDeepRightAll} from '~/modules/module_utils'

import * as types from './constants'

let configInitialState = {
  guys: [],
  girls: [],
  assigned_guys: [],
  assigned_girls: [],
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
    case types.UPDATE_COUPLES: {
      return {...state, couples: action.payload}
    }
    case types.ADD_COUPLE:
      return {
        ...state,
        couples: [...state.couples, action.payload]
      }
    case types.REMOVE_COUPLE: {
      const {idx} = action.payload
      return {
        ...state,
        couples: state.couples.filter((c,i) => i != idx)
      }
    }
    case types.COUPLE_CHANGE_SINGLES: {
      const {idx, value} = action.payload
      return {
        ...state,
        couples: state.couples.map((c,i) => {
          if (i === idx) {
            return {...c, as_singles: value}
          }
          return c
        })
      }
    }
    case types.COUPLE_CHANGE_FULLTIME: {
      const {idx, value} = action.payload
      return {
        ...state,
        couples: state.couples.map((c,i) => {
          if (i === idx) {
            return {...c, fulltime: value}
          }
          return c
        })
      }
    }
    case types.COUPLE_CHANGE_NAME: {
      const {idx, value} = action.payload
      return {
        ...state,
        couples: state.couples.map((c,i) => {
          if (i === idx) {
            return {...c, name: value}
          }
          return c
        })
      }
    }
    default:
      return state
  }
}

export default mainReducer
