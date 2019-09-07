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
      
      return {
        ...state,
        couples: [...state.couples]
      }
    }
    case types.COUPLE_CHANGE_SINGLES: {
      const {id, value} = action.payload
      return {
        ...state,
        couples: state.couples.map(c => {
          if (c.id == id) {
            return {...c, as_singles: value}
          }
          return c
        })
      }
    }
    case types.COUPLE_CHANGE_FULLTIME: {
      const {id, value} = action.payload
      return {
        ...state,
        couples: state.couples.map(c => {
          if (c.id == id) {
            return {...c, fulltime: value}
          }
          return c
        })
      }
    }
    case types.COUPLE_CHANGE_NAME: {
      const {id, name} = action.payload
      return {
        ...state,
        couples: state.couples.map(c => {
          if (c.id == id) {
            return {...c, name: name}
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
