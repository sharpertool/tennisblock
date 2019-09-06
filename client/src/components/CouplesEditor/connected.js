import React from 'react'
import {connect} from 'react-redux'
import {selectors, actions} from '~/redux-page'

import CouplesEditor from './index'

const connectedComponent = ({
                              guys,
                              girls,
                              couples,
                            }) => {
  return (
    <CouplesEditor
      guys={guys}
      girls={girls}
    />
  )
}

const mapStateToProps = (state) => {
  return {
    guys: selectors['season:getGuys'](state),
    girls: selectors['season:getGirls'](state),
    couples: selectors['season:getCouples'](state),
  }
}

const dispatchActions = {}

export default connect(mapStateToProps, dispatchActions)(connectedComponent)
