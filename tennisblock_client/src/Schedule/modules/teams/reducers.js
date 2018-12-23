// If a feature has more facets, you should definitely use multiple
// reducers to handle different parts of the state shape.
// Additionally, don’t be afraid to use combineReducers as much as needed.
// This gives you a lot of flexibility when working with a complex state shape.
import * as types from './constants'

const initialState = {
  blockplayers: {},
  schedule: [],
  subs: {},
  ui: {
    selected: null
  }
}

const mainReducer = (state = initialState, action) => {
  const { blockplayers, subs } = action
  switch(action.type) {
    case types.UPDATE_PLAY_SCHEDULE:
      return {...state}
      break
    case types.BLOCK_PLAYERS_FETCHED:
      return { ...state, blockplayers }
      break
    case types.UPDATE_MATCH_DATA:
      return {...state, schedule: action.payload}
    case types.CALCULATE_MATCHUPS:
      return {...state, schedule: []}
    case types.GET_SUBS:
      return { ...state, subs }
      break
    default: return state
  }
}

export default mainReducer
