import { handleActions } from 'redux-actions'
import * as types from './constants'

const initialState = {
  current_meeting: {
    date: null,
    players_by_id: {},
    guys: [],
    gals: [],
  },
  current_date: null,
  players_by_id: {},
  curr_guys: [],
  curr_gals: [],
  original_guys: [],
  original_gals: [],

  originalCouples: [],
  meeting_dates: [],
  subs_guys: [],
  subs_gals: []
}

const filter_sub = (sub) => {
  return sub.id
}
const filter_player = (p) => {
  const {name, id} = p
  return {name, id}
}

const player_by_id_update = (pbid, players) => {
  const more = players.reduce((acc, p) => {
    acc[p.id] = {
      name: p.name,
      id: p.id,
      ntrp: p.ntrp,
      untrp: p.untrp,
      gender: p.gender,
    }
    return acc
  }, {})
  return {...pbid, ...more}
}

const reducer = handleActions(
    {
        [types.SET_BLOCKDATES](state, { payload }) {
          return {
            ...state,
            meeting_dates: payload
          }
        },

        [types.UPDATE_PLAY_SCHEDULE](state, { payload }) {
          return {...state}
        },

        [types.SET_BLOCK_PLAYERS](state, { payload }) {
          const {date, guys, gals} = payload
          const processed = [...guys, ...gals].reduce((acc, p) => {
            acc.players_by_id[p.id] = {
              name: p.name,
              id: p.id,
              ntrp: p.ntrp,
              untrp: p.untrp,
              gender: p.gender,
            }
            if (p.gender === 'm') {
              acc.curr_guys.push(p.id)
              acc.original_guys.push(p.id)
            } else {
              acc.curr_gals.push(p.id)
              acc.original_gals.push(p.id)
            }
            return acc
          }, {
            players_by_id:{},
            curr_guys: [],
            curr_gals:[],
            original_guys: [],
            original_gals: [],
          })

          return {
            ...state,
            ...processed,
            current_date: date,
            //originalCouples: [...couples],
            guys: guys.map(filter_player),
            gals: gals.map(filter_player),
          }
        },

        [types.SET_SUBS](state, { payload }) {
          const subs = payload
          const {guysubs: guys, galsubs: gals} = payload
          return {
            ...state,
            subs_guys: guys.map(s => s.id),
            subs_gals: gals.map(s => s.id),
            players_by_id: player_by_id_update(state.players_by_id, [...guys, ...gals])
          }
        },

        [types.BLOCK_PLAYER_CHANGED](state, { payload }) {
          const { group, value, previous } = payload
          const [key,skey] = [`curr_${group}`, `subs_${group}`]

          // Making a copy of arrays so result is immutable.
          let curr = state[key].slice()
          let subs = state[skey].slice()

          const idx = curr.indexOf(previous)
          const sidx = subs.indexOf(value)

          curr.splice(idx > -1 ? idx : curr.length, 1, value)
          subs.splice(sidx, 1, idx > -1 ? previous : null)

          return {
            ...state,
            [key]: curr,
            [skey]: subs
          }
        },
    },
    initialState
)

export default reducer
