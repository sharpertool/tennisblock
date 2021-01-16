import React from 'react'
import {connect} from 'react-redux'
import {withRouter} from 'react-router-dom'
import {selectors, actions} from '~/redux-page'

import MeetingMatchups from './index'

const mapStateToProps = (state) => {
  return {
    calcResults: selectors.calcResult(state),
    validPlaySchedule: selectors.validPlaySchedule(state),
    iterations: selectors.get_iterations(state),
    tries: selectors.get_tries(state),
    fpartner: selectors.get_fpartner(state),
    fteam: selectors.get_fteam(state),
    low_threshold: selectors.get_low_threshold(state),
    match_count: selectors.get_match_count(state),
  }
}

const mapDispatchToProps = ({
  getBlockPlayers: actions.getBlockPlayers,
  calculateMatchups: actions.calculateMatchups,
  recalculateMatch: actions.recalculateMatch,
  updateCalcValue: actions.updateCalcValue,
  fetchCurrentSchedule: actions['teams:fetchCurrentSchedule'],
})

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingMatchups))
