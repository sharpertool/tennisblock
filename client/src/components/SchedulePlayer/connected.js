import React  from 'react'
import {connect} from 'react-redux'
import {actions, selectors} from '~/redux-page'

import SchedulePlayer from './index'

const mapStateToProps = (state, props) => {
  return {
    verifyCode: selectors['schedule:verifyCode'](state, props.id),
  }
}

const mapDispatchToProps = {
  onBlockPlayerChanged: actions['schedule:onBlockPlayerChanged'],
  verifyPlayer: actions['schedule:manualVerifyPlayer'],
  notifyPlayer: actions['schedule:notifyPlayer'],
}

export default connect(mapStateToProps, mapDispatchToProps)(SchedulePlayer)
