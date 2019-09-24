import React, {Component} from 'react'
import {connect} from 'react-redux'
import {actions, selectors} from '~/redux-page'

import SchedulePlayer from './index'

const mapStateToProps = (state, props) => {
  return {
    verifyCode: selectors['schedule:verifyCode'](state, props.id),
  }
}

console.dir(actions)
const mapDispatchToProps = {
  onPlayerChanged: actions.onPlayerChanged,
  verifyPlayer: actions['schedule:manualVerifyPlayer'],
  notifyPlayer: actions['schedule:notifyPlayer'],
}


export default connect(mapStateToProps, mapDispatchToProps)(SchedulePlayer)
