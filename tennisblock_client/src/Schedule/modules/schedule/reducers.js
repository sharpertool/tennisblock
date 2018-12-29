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

const filter_sub = (sub) => {
  const {name, id} = sub
  return {name, id}
}
const filter_player = (p) => {
  const {name, id} = p
  return {name, id}
}

const reducer = handleActions(
    {
        [types.SET_BLOCKDATES](state, { payload }) {
          const blockdates = payload
          return {
            ...state,
            blockdates
          }
        },

        [types.UPDATE_PLAY_SCHEDULE](state, { payload }) {
          return {...state}
        },

        [types.FETCH_BLOCK_PLAYERS_SUCCEED](state, { payload }) {
          const blockplayers = payload
          const { couples, guys, gals } = blockplayers

          return {
            ...state,
            blockplayers,
            originalCouples: [...couples],
            guys: guys.map(filter_player),
            gals: gals.map(filter_player),
          }
        },

        [types.GET_SUBS](state, { payload }) {
          const subs = payload
          const {guysubs: guys, galsubs: gals} = payload
          return {
            ...state,
            subs,
            subs_guys: guys.map(filter_sub),
            subs_gals: gals.map(filter_sub),
          }
        },

        [types.BLOCK_PLAYER_CHANGED](state, { payload }) {
          const selectedPlayer = payload
          const { key, gender, player } = selectedPlayer
          const currentPlayer = state.blockplayers.couples[key][gender]

          state.blockplayers.couples.splice(key, 1, {
            ...state.blockplayers.couples[key],
            [gender]: player
          })

          const subIndex = state.subs[`${gender}subs`].findIndex(sub => sub.id === selectedPlayer.player.id)
          state.subs[`${gender}subs`].splice(subIndex, 1, currentPlayer)

          return { ...state }
        },


    },
    initialState
)

export default reducer
