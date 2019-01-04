import {isEqual} from 'lodash'
export const blockUpdates = ({ blockUpdates }) => ({ ...blockUpdates })

export const getBlockPlayers = ({ blockplayers }) => (blockplayers)

export const getCouples = state => {
  const {players_by_id: pbid, curr_guys: guys, curr_gals: gals} = state
  const n = Math.max(guys.length, gals.length)
  const couples = [...Array(n).keys()].map(() => (
    {guy: null, gal: null}
    )
  )
  gals.map((g, i) => {
    couples[i].gal = {id: g, name:pbid[g].name}
  })
  guys.map((g, i) => {
    couples[i].guy = {id: g, name:pbid[g].name}
  })
  console.log(`Couples: ${JSON.stringify(couples)}`)
  return couples
}

export const currentDate = state => state.current_date

export const getGuySubs = state => {
  const {players_by_id: pbid, subs_guys: s} = state
  return s.map(id => {
    const p = pbid[id]
    if (p !== 'undefined') {
      return {id: id, name: p.name}
    }
    return null
  })
}

export const getGalSubs = state => {
  const {players_by_id: pbid, subs_gals: s} = state
  return s.map(id => {
    const p = pbid[id]
    if (p !== 'undefined') {
      return {id: id, name: p.name}
    }
    return null
  })
}

export const getSubs = state => {
  return {
    guys: getGuySubs(state),
    gals: getGalSubs(state)
  }
}

export const players_by_id = state => state.players_by_id

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
  return state.curr_guys.length != 0 &&state.curr_gals.length != 0
}

export const canReSchedule = state => {
  return state.curr_guys.length != 0 &&state.curr_gals.length != 0
}

export const canUpdateSchedule = state => {
  return state.curr_guys.length != 0 &&state.curr_gals.length != 0
}
