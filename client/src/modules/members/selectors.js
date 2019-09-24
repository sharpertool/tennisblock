import {createSelector} from 'reselect'

export const blockmembers = state => state.blockmembers
const players = state => state.allplayers

export const players_by_id = createSelector(
  players,
  players => {
    return players.reduce((a, player) => {
      a[player.pk] = player
      return a
    }, {})
  }
)
export const members_by_id = createSelector(
  blockmembers,
  players => {
    return players.reduce((a, player) => {
      a[player.id] = player
      return a
    }, {})
  }
)

export const subs = createSelector(
  players, blockmembers,
  (players, blockmembers) => {
    const sub_ids = blockmembers.reduce((a,bm) => {
      if (!bm.blockmember) {
        a.push(bm.id)
      }
      return a
    }, [])
    return sub_ids
  }
)

export const more_players = createSelector(
  players, blockmembers,
  (players, blockmembers) => {
    const member_ids = blockmembers.reduce((a,bm) => {
      a.push(bm.id);
      return a
    }, [])
    const sub_players = players.filter(p => {
      return !(member_ids.includes(p.pk))
    })
    return sub_players.reduce((a, s) => {
      a.push(s.pk)
      return a
    }, [])
  }
)

export const getMemberById = (state, id) => members_by_id(state)[id]
export const getPlayerById = (state, id) => players_by_id(state)[id]

