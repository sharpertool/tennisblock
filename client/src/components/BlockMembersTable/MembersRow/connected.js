import React from 'react'
import {connect} from 'react-redux'
import {selectors, actions} from '~/redux-page'

import Member from './index'

const connectedComponent = ({
                              member,
                              player,
                              onBlockmemberChange,
                            }) => {
  return (
    <Member
      member={member}
      player={player}
      onBlockmemberChange={onBlockmemberChange}
    />
  )
}

const mapStateToProps = (state, props) => {
  return {
    player: selectors['members:getPlayerById'](state, props.id),
    member: selectors['members:getMemberById'](state, props.id),
  }
}

const mapDispatchToProps = {
  onBlockmemberChange: actions['members:onBlockMemberChanged'],
}

export default connect(mapStateToProps, mapDispatchToProps)(connectedComponent)
