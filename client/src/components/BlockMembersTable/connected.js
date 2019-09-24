import React from 'react'
import {connect} from 'react-redux'
import {selectors, actions} from '~/redux-page'

import BlockMembers from './index'

const connectedComponent = ({
                              blockmembers,
  subs,
  moreplayers,
                              onBlockmemberChange,
                            }) => {
  return (
    <BlockMembers
      blockmembers={blockmembers}
      subs={subs}
      moreplayers={moreplayers}
      onBlockmemberChange={onBlockmemberChange}
    />
  )
}

const mapStateToProps = (state) => {
  return {
    blockmembers: selectors['members:blockmembers'](state),
    subs: selectors['members:subs'](state),
    moreplayers: selectors['members:more_players'](state),
  }
}

const mapDispatchToProps = {
  onBlockmemberChange: actions['members:onBlockMemberChanged'],
}

export default connect(mapStateToProps, mapDispatchToProps)(connectedComponent)
