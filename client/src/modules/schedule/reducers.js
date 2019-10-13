import clone from 'ramda/src/clone'
import {mergeDeepRightAll} from '~/modules/module_utils'
import * as R from 'ramda'
import {handleActions} from 'redux-actions'
import * as types from './constants'
import {
  groupByGenderAndId,
  toObjectById
} from './ramda_utils'

let configInitialState = {
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
  subs_gals: [],
  
  // Notification
  notify_errors: [],
  notify_message: '',
  notify_in_progress: false,
  
  // Verification
  verify_status_by_id: {},
}

export const update_initial_state = (initial_state) => {
  configInitialState = mergeDeepRightAll(configInitialState, initial_state)
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
    [types.SET_CURRENT_DATE](state, {payload}) {
      return {...state, current_date: payload.date}
    },
    [types.SET_BLOCKDATES](state, {payload}) {
      return {
        ...state,
        meeting_dates: payload
      }
    },
    
    [types.UPDATE_PLAY_SCHEDULE](state, {payload}) {
      return {...state}
    },
    
    [types.SET_BLOCK_PLAYERS](state, {payload}) {
      const {date, guys, gals, couples} = payload
      const nCourts = couples.length * 2
      // Some Ramda approaches, just testing for now
      const players_by_id = toObjectById(R.concat(guys, gals))
      //const curr = groupByGenderAndId(players_by_id)
      
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
        players_by_id: {},
        curr_guys: [],
        curr_gals: [],
        original_guys: [],
        original_gals: [],
      })
      
      if (processed.curr_guys.length == 0) {
        const tmp = [
          ...Array(nCourts / 2).keys()
        ].map(() => -1)
        processed.curr_guys = R.clone(tmp)
        processed.curr_gals = R.clone(tmp)
        processed.original_guys = R.clone(tmp)
        processed.origial_gals = R.clone(tmp)
      }
      
      return {
        ...state,
        ...processed,
        pbyid: players_by_id,
        //originalCouples: [...couples],
        guys: guys.map(filter_player),
        gals: gals.map(filter_player),
      }
    },
    
    [types.SET_SUBS](state, {payload}) {
      const subs = payload
      const {guysubs: guys, galsubs: gals} = payload
      return {
        ...state,
        subs_guys: guys.map(s => s.id),
        subs_gals: gals.map(s => s.id),
        players_by_id: player_by_id_update(state.players_by_id, [...guys, ...gals])
      }
    },
    
    [types.BLOCK_PLAYER_CHANGED](state, {payload}) {
      const {group, index, value, previous} = payload
      const [key, skey] = [`curr_${group}`, `subs_${group}`]
      
      console.log(`Change ${group} idx:${index} from ${previous} to ${value}`)
      // Making a copy of arrays so result is immutable.
      let curr = state[key].slice()
      let subs = state[skey].slice()
      
      // Use the index from the original value.
      // This may
      const prev = curr.splice(index, 1, value)
      
      // Remove new player from subs
      subs = subs.filter(id => id != value)
      if (previous != -1) {
        subs.push(previous)
      }
      
      return {
        ...state,
        [key]: curr,
        [skey]: subs
      }
    },
    
    [types.SCHEDULE_VERIFY_CHANGED](state, {payload}) {
      const newstatus = {...state.verify_status_by_id}
      const code = payload.status == 'verified' ? 'C' : 'R'
      newstatus[payload.user_id] = code
      return {
        ...state,
        verify_status_by_id: newstatus
      }
    },
    
    [types.SCHEDULE_NOTIFY_MSG_UPDATE](state, {payload}) {
      console.log(`Message updated to ${payload}`)
      return {
        ...state,
        notify_message: payload
      }
    },
    
    [types.SCHEDULE_NOTIFY_STARTED](state, {payload}) {
      return {
        ...state,
        notify_in_progress: true,
        notify_errors: [],
      }
    },
    [types.SCHEDULE_NOTIFY_SUCCESS](state, {payload}) {
      return {
        ...state,
        notify_in_progress: false,
        notify_errors: [],
      }
    },
    [types.SCHEDULE_NOTIFY_FAIL](state, {payload}) {
      return {
        ...state,
        notify_in_progress: false,
        notify_errors: payload,
      }
    },
    [types.UPDATE_VERIFY_STATUS](state, {payload}) {
      return {
        ...state,
        verify_status_by_id: payload
      }
    }
  },
  clone(configInitialState),
)

export default reducer
