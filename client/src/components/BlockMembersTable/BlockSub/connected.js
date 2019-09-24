import React from 'react'
import {connect} from 'react-redux'
import {selectors, actions} from '~/redux-page'

import BlockSub from './index'

const connectedComponent = (props) => {
  return (
    <BlockSub
      {...props}
    />
  )
}

const mapStateToProps = (state, props) => {
  return {
    player: selectors['members:getPlayerById'](state, props.id),
  }
}

const mapDispatchToProps = {
  toggleBlockSub: actions['members:toggleBlockSub'],
}

export default connect(mapStateToProps, mapDispatchToProps)(connectedComponent)
