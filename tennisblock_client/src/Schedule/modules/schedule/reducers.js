import { handleActions } from 'redux-actions'
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

const reducer = handleActions(
    {
        [types.SET_BLOCKDATES](state, { payload }) {
          const { blockdates } = payload
          return {
            ...state,
            blockdates
          }
        },

        [types.UPDATE_PLAY_SCHEDULE](state, { payload }) {
          return {...state}
        },

        [types.FETCH_BLOCK_PLAYERS_SUCCEED](state, { payload }) {
          const { blockplayers } = payload
          const { couples } = blockplayers

          return {
            ...state,
            blockplayers,
            originalCouples: Object.assign({}, couples)
          }
        },

        [types.GET_SUBS](state, { payload }) {
          const { subs } = payload
          return {
            ...state,
            subs
          }
        },

        [types.BLOCK_PLAYER_CHANGED](state, { payload }) {
          const { selectedPlayer } = payload
          const { key, gender, player } = selectedPlayer

          state.blockplayers.couples.splice(key, 1, {
            ...state.blockplayers.couples[key],
            [gender]: player
          })

          return { ...state }
        },


    },
    initialState
)

export default reducer
