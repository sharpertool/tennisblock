import * as types from './constants'

const initialState = {
  season: {
    name: '',
    start: null,
    end: null,
    weekday: null,
    time: null,
    meetings: []
  },

  current_meeting: {
    date: null,
    players_by_id: {},
    guys: [],
    gals: [],
  },
  blockdates: [],
}


const mainReducer = (state = initialState, action) => {
  const { blockdates } = action
  switch(action.type) {
    case types.SET_BLOCKDATES: 
      return {
        ...state,
        blockdates
      }
    default: return state;
  }

}

export default mainReducer
