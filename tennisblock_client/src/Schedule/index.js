import React from 'react'
import {render} from 'react-dom'
import {Provider} from 'react-redux'

import './index.scss'

// Build the Store stuff
import makeStore from 'Schedule/modules'

import MatchReview from './matchreview'
import * as types from "./modules/teams/constants"

export default ({match_review}) => {
  const store = makeStore(null, null)
  
  const onDateChanged = (currdate) => {
    console.log(`onDateChanged called with ${currdate}`)
    store.dispatch({
      type: 'UPDATE_CURRENT_DATE',
      payload: currdate
    })
    console.log('onDateChanged dispatched action')
  }
  
  console.log(`Mounting at ${match_review}`)
  render(<MatchReview store={store}/>, document.getElementById(match_review))
  console.log('Schedule React component mounted')
  return onDateChanged
}