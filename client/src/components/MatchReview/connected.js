import React from 'react'
import {connect} from 'react-redux'

import {actions, selectors} from '~/redux-page'

import MatchReview from './index'

const mapStateToProps = (state) => {
  return {
    play_schedule: selectors.playSchedule(state)
  }
}

/**
 * Object with key/values for dispatch actions
 *
 * connect will bind these to disptch, but I don't know if that
 * will support actions with values.
 * @type {{clickOptions: toggleOptions}}
 */
const dispatchActions = {
  recalculateMatch: actions.recalculateMatch
}


export default connect(mapStateToProps, dispatchActions)(MatchReview)
