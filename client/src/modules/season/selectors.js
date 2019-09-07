import {createSelector} from 'reselect'
import {memoizeWith} from 'ramda'

const guys = state => state.guys
const girls = state => state.girls
const couples = state => state.couples

export const guysById = createSelector(
  guys,
  guys => {
    return guys.reduce((acc, guy) => {
      acc[guy.id] = guy
      return acc
    }, {})
  }
)

export const girlById = createSelector(
  girls,
  girls => {
    return girls.reduce((acc, guy) => {
      acc[guy.id] = guy
      return acc
    }, {})
  }
)

export const getCouples = createSelector(
  guysById, girlById, couples,
  (guysById, girlById, couples) => {
    return couples.map(c => {
      return {...c, girl:girlById[c.girl], guy: guysById[c.guy]}
    })
  }
)

export const getGuys = createSelector(
  guys,
  couples,
  (guys, couples) => {
    const assigned_ids = couples.map(c => c.guy)
    const available = guys.filter(g => !assigned_ids.includes(g.id))
    return available
  }
)

export const getGirls = createSelector(
  girls,
  couples,
  (girls, couples) => {
    const assigned_ids = couples.map(c => c.girl)
    const available = girls.filter(g => !assigned_ids.includes(g.id))
    return available
  }
)

