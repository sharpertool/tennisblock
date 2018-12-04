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
  originalCouples: [],
  blockdates: [],
  blockplayers: {},
  subs: {},
}


const mainReducer = (state = initialState, action) => {
  const { blockdates, blockplayers, subs, couples, selectedValue } = action
  switch(action.type) {
    case types.SET_BLOCKDATES:
      return {
        ...state,
        blockdates
      }
    case types.UPDATE_PLAY_SCHEDULE:
      return {...state}
      break
    case types.BLOCK_PLAYERS_FETCHED:
      return { ...state, blockplayers }
      break
    case types.GET_SUBS:
      return { ...state, subs }
      break
    case types.COPY_ORIGINAL_COUPLES:
      return {
        ...state,
        originalCouples: Object.assign({}, couples)
      }
      break
    case types.UPDATE_COUPLE:
      const { index, gender, player } = action.selectedValue
      state.blockplayers.couples.splice(index, 1, {
        ...state.blockplayers.couples[index],
        [gender]: player
      })
      return { ...state }
      break
    default: return state;
  }

}

export default mainReducer
