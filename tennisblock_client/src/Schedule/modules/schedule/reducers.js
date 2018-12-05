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
  const { payload } = action

  switch(action.type) {
    case types.SET_BLOCKDATES:
      const { blockdates } = payload
      return {
        ...state,
        blockdates
      }
      break

    case types.UPDATE_PLAY_SCHEDULE:
      return {...state}
      break

    case types.FETCH_BLOCK_PLAYERS_SUCCEED:
      const { blockplayers } = payload
      const { couples } = blockplayers

      return {
        ...state,
        blockplayers,
        originalCouples: Object.assign({}, couples)
      }
      break

    case types.GET_SUBS:
      const { subs } = payload
      return {
        ...state,
        subs
      }
      break

    case types.BLOCK_PLAYER_CHANGED:
      const { selectedPlayer } = payload
      const { key, gender, player } = selectedPlayer
      state.blockplayers.couples.splice(key, 1, {
        ...state.blockplayers.couples[key],
        [gender]: player
      })
      return { ...state }
      break

    default: return state;
  }

}

export default mainReducer
