import {selectors} from '~/Schedule/modules/schedule'
import * as R from 'ramda'

describe('Insure selectors return valid stuff', () => {
  
  const players = [
      {id: 20, name: 'Ed', gender: 'm'},
      {id: 6, name: 'Jake', gender: 'm'},
      {id: 30, name: 'Bob', gender: 'm'},
      {id: 31, name: 'Kitty', gender: 'f'},
      {id: 32, name: 'Randy', gender: 'f'},
      {id: 33, name: 'Kris', gender: 'f'},
  ]
  const subs = [
      {id: 40, name: 'Jack', gender: 'm'},
      {id: 41, name: 'Ted', gender: 'm'},
      {id: 42, name: 'Fred', gender: 'm'},
      {id: 43, name: 'Anne', gender: 'f'},
      {id: 44, name: 'Kathy', gender: 'f'},
      {id: 45, name: 'Ellen', gender: 'f'},
    
  ]
  
  const state = {
    players_by_id: {},
    curr_guys: [],
    curr_gals: [],
  }
  
  it('should return couples', () => {
    const c = selectors.getCouples({})
    
    expect(c).toBe({couples: []})
  })
  
})
