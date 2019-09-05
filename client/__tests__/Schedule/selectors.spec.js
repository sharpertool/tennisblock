import {getCouples} from '~/modules/schedule/selectors'

describe('Insure selectors return valid stuff', () => {
  
  const players = [
      {id: 20, name: 'Ed'},
      {id: 6, name: 'Jake'},
      {id: 30, name: 'Bob'},
      {id: 31, name: 'Kitty'},
      {id: 32, name: 'Randy'},
      {id: 33, name: 'Kris'},
      {id: 40, name: 'Jack'},
      {id: 41, name: 'Ted'},
      {id: 42, name: 'Fred'},
      {id: 43, name: 'Anne'},
      {id: 44, name: 'Kathy'},
      {id: 45, name: 'Ellen'},
  ]
  const subs = [
  ]
  
  const byid = players.reduce((acc, p) => {
      acc[p.id] = p
      return acc
    }, {})
  
  const state = {
    current_date: 'current',
    meeting_dates: [{date: 'current', num_courts: 2}],
    players_by_id: byid,
    curr_guys: [20, 6, 40, 41],
    curr_gals: [31, 33, 43, 44],
  }
  
  it('should return couples', () => {
    const c = getCouples(state)
    
    const expected = state.curr_gals.map((gid, idx) => {
      return {gal: byid[gid], guy: byid[state.curr_guys[idx]]}
    })
    expect(c).toStrictEqual(expected)
  })
  
})
