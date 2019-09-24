import React from 'react'
import {connect} from 'react-redux'
import {selectors, actions} from '~/redux-page'

import BlockMembers from './index'

const connectedComponent = ({
                              blockmembers,
                              onBlockmemberChange,
                            }) => {
  return (
    <BlockMembers
      blockmembers={blockmembers}
      onBlockmemberChange={onBlockmemberChange}
    />
  )
}

const mapStateToProps = (state) => {
  return {
    blockmembers: selectors['members:blockmembers'](state),
  }
}

const mapDispatchToProps = {
  onBlockmemberChange: actions['members:onBlockMemberChanged'],
}

export default connect(mapStateToProps, mapDispatchToProps)(connectedComponent)
