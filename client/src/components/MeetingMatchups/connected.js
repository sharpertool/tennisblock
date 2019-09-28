import React from 'react'
import {connect} from 'react-redux'
import {withRouter} from 'react-router-dom'
import {selectors, actions} from '~/redux-page'

import MeetingMatchups from './index'

const mapStateToProps = (state) => {
  return {
    calcResults: selectors.calcResult(state),
    validPlaySchedule: selectors.validPlaySchedule(state)
  }
}

const mapDispatchToProps = ({
  getBlockPlayers: actions.getBlockPlayers,
  calculateMatchups: actions.calculateMatchups,
  fetchCurrentSchedule: actions['teams:fetchCurrentSchedule'],
})

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingMatchups))
