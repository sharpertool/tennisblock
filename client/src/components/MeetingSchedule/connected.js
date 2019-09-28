import React from 'react'
import {connect} from 'react-redux'
import {withRouter} from 'react-router-dom'

import {actions, selectors} from '~/redux-page'

import MeetingSchedule from './index'

const mapStateToProps = (state) => {
  return {
    couples: selectors.getCouples(state),
    canClearSchedule: selectors.canClearSchedule(state),
    canReSchedule: selectors.canReSchedule(state),
    canUpdateSchedule: selectors.isScheduleChanged(state),
  }
}

const mapDispatchToProps = {
  getBlockPlayers: actions.getBlockPlayers,
  updateBlockPlayers: actions.updateBlockPlayers,
  clearSchedule: actions.clearSchedule,
  onReSchedule: actions.reSchedule,
  onNotify: actions.scheduleNotify,
}

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingSchedule))
