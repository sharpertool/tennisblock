// If a feature has more facets, you should definitely use multiple
// reducers to handle different parts of the state shape.
// Additionally, don’t be afraid to use combineReducers as much as needed.
// This gives you a lot of flexibility when working with a complex state shape.
import {combineReducers} from 'redux'
import * as types from './constants'

const initialState = {
  schedule: []
}

const mainReducer = (state = initialState, action) => {
  switch(action.type) {
    case types.UPDATE_PLAY_SCHEDULE:
      return {...state, schedule: action.payload.match}
    default: return state;
  }
}

export default mainReducer
