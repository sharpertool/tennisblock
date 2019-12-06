import {isEqual} from 'lodash'
import {createSelector} from 'reselect'

export const current_date = state => state.current_date
export const meeting_dates = state => state.meeting_dates
export const curr_guys = state => state.curr_guys
export const curr_gals = state => state.curr_gals
export const couples = state => state.couples

export const players_by_id = state => state.players_by_id
export const blockUpdates = ({ blockUpdates }) => ({ ...blockUpdates })
export const getBlockPlayers = ({ blockplayers }) => (blockplayers)
export const getVerifyStatus = state => state.verify_status_by_id

export const court_count = state => state.num_courts

export const currentMeeting = createSelector(
  [current_date, meeting_dates],
  (current_date, meeting_dates) => {
    const mtgs = meeting_dates.filter(m => m.date == current_date)
    if (mtgs.length > 0) {
      return mtgs[0]
    }
    return null
  }
)

export const verifyCode = (state, id) => getVerifyStatus(state)[id]

export const getCouples2 = createSelector(
  [players_by_id, couples, court_count],
  (players_by_id, couples, court_count) => {
    const dummy = {id: -1, name: '---'}
    let tmp = couples.map(couple => {
      return {
        'guy': couple[0] != -1 ? players_by_id[couple[0]] : dummy,
        'gal': couple[1] != -1 ? players_by_id[couple[1]] : dummy,
      }
    })
    if (tmp.length < court_count*2) {
      const dummies = [...Array(court_count*2-tmp.length).keys()].map(
        () => { return {'gal': dummy, 'guy': dummy}}
      )
      tmp = [...tmp, ...dummies]
    }
   return tmp
  }
)

export const getCouples = state => {
  const {players_by_id: pbid,
    curr_guys: guys,
    curr_gals: gals} = state
  const num_courts = court_count(state)
  // We  need 2 couples per court, so num_courts * 2
  const n = Math.max(guys.length, gals.length)
  const couple_cnt = Math.max(num_courts*2, gals.length, guys.length)
  const couples = [...Array(couple_cnt).keys()].map(() => (
    {guy: {id: -1, name:'---'}, gal: {id:-1, name:'---'}}
    )
  )
  gals.map((g, i) => {
    const couple = couples[i]
    if (g == -1) {
      couple.gal = {id: -1, name:'---'}
    } else {
      couple.gal = {id: g, name:pbid[g].name}
    }
  })
  guys.map((g, i) => {
    const couple = couples[i]
    if (g == -1) {
      couple.guy = {id: -1, name:'---'}
    } else {
      couple.guy = {id: g, name: pbid[g].name}
    }
  })
  return couples
}

export const getScheduledPlayers = state => {
  return {
    guys: state.curr_guys,
    girls: state.curr_gals,
  }
}

// Notification
export const notify_message = state => state.notify_message
export const notify_errors = state => state.notify_errors


export const currentDate = state => state.current_date

export const getGuySubs = state => {
  const {players_by_id: pbid, subs_guys: s} = state
  return s.reduce((subs, id) => {
    const p = pbid[id]
    if (p) {
      subs.push({id: id, name: p.name})
    }
    return subs
  }, [])
}

export const getGalSubs = state => {
  const {players_by_id: pbid, subs_gals: s} = state
  return s.reduce((subs, id) => {
    const p = pbid[id]
    if (p) {
      subs.push({id: id, name: p.name})
    }
    return subs
  }, [])
}

export const getSubs = state => {
  return {
    guys: getGuySubs(state),
    gals: getGalSubs(state)
  }
}


export const isScheduleChanged = state => {
  const {
    curr_guys: cguys,
    curr_gals: cgals,
    original_guys: oguys,
    original_gals: ogals
  } = state
  return !isEqual(oguys, cguys) || !isEqual(ogals, cgals)
}

export const changes = state => {
  return {}
}

export const canClearSchedule = state => {
  return state.curr_guys.length != 0 && state.curr_gals.length != 0
}

export const canReSchedule = state => {
  return state.curr_guys.every(v => v === -1) && state.curr_gals.every(v => v === -1)
}

export const canUpdateSchedule = state => {
  return state.curr_guys.length != 0 &&state.curr_gals.length != 0
}
