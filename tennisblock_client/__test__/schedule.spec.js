import { createAction } from 'redux-actions'
import sch_init from '../src/Schedule'

describe('action tests', () => {
  it('creates a valid simple action', () => {
    const a = createAction('Ballyhoo')
    const anaction = a()
    expect(anaction).toEqual({'type': 'Ballyhoo'})
  })

  it('creates a valid complex action', () => {
    const a = createAction('Ballyhoo')
    const data = {'some': {'data': [1,2,3]}}
    const anaction = a(data)
    expect(anaction).toEqual({'type': 'Ballyhoo', 'payload': data})
  })
})

describe('test init function', () => {
  it('should render an element', () => {
    document.body.innerHTML =
      `<div id="root">
          <span id="username"/>
          <span id="button"/>
      </div>`
    
    sch_init({target:'root'})
    
    
  })
})