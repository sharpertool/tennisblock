import React from 'react'
import {connect} from 'react-redux'
import {withRouter} from 'react-router-dom'

import {actions, selectors} from '~/redux-page'

import MeetingSchedule from './index'

const mapStateToProps = (state) => {
  return {
    couples: selectors['schedule:getCouples2'](state),
    canClearSchedule: selectors.canClearSchedule(state),
    canReSchedule: selectors.canReSchedule(state),
    canUpdateSchedule: selectors.isScheduleChanged(state),
  }
}

const mapDispatchToProps = {
  getBlockPlayers: actions['schedule:getBlockPlayers'],
  updateBlockPlayers: actions['schedule:updateBlockPlayers'],
  clearSchedule: actions['schedule:clearSchedule'],
  onReSchedule: actions['schedule:reSchedule'],
  onNotify: actions['schedule:scheduleNotify'],
  onDateChange: actions['schedule:setCurrentDate'],
}

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingSchedule))
