// If a feature has more facets, you should definitely use multiple
// reducers to handle different parts of the state shape.
// Additionally, don’t be afraid to use combineReducers as much as needed.
// This gives you a lot of flexibility when working with a complex state shape.
import * as types from './constants'

const initialState = {
  schedule: [],
  schedule_result: {
    status: '',
    error: null
  },
  iterations: 35,
  tries: 45,
  fpartner: 1.5,
  fteam: 3.5,
  low_threshold: 0.75,
}

const mainReducer = (state = initialState, action) => {
  const {blockplayers, subs} = action
  switch (action.type) {
    case types.UPDATE_PLAY_SCHEDULE:
      return {...state}
      break
    case types.UPDATE_CALC_VALUE: {
      const {name, value} = action.payload
      const new_state = {...state}
      new_state[name] = value
      return new_state
    }
    case types.UPDATE_CALCULATE_STATUS:
      return {...state, schedule_result: action.payload}
    case types.BLOCK_PLAYERS_FETCHED:
      return {...state, blockplayers}
      break
    case types.UPDATE_MATCH_DATA:
      return {...state, schedule: action.payload}
    case types.CALCULATE_MATCHUPS:
      return {
        ...state,
        schedule: [],
        schedule_result: {'status': null, error: null}
      }
    case types.GET_SUBS:
      return {...state, subs}
      break
    default:
      return state
  }
}

export default mainReducer
