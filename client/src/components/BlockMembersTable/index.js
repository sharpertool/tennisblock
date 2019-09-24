import React from 'react'

import MembersHeader from './MembersHeader'
import SubsHeader from './SubsHeader'
import Member from './MembersRow/connected'
import BlockSub from './BlockSub/connected'

const BlockMembers = ({
                        blockmembers,
                        subs,
                        moreplayers,
                        onBlockmemberChange,
                      }) => {
  return (
    <div id='members' className={'members'}>
      <table className={'member_list table'}>
        <MembersHeader
        />
        <tbody>
        {blockmembers.map((member, idx) => {
          return (<Member
            key={idx}
            even={idx % 2 == 0}
            id={member.id}
            onBlockmemberChange={onBlockmemberChange}
          />)
        })}
        </tbody>
      </table>
      <table className={'members table'}>
        <SubsHeader
        />
        <tbody>
        {subs.map((player, idx) => {
          return <BlockSub
            key={player}
            id={player}
            can_add={false}
          />
        })}
        </tbody>
      </table>
      
      <table className={'members table'}>
        <SubsHeader
        />
        <tbody>
        {moreplayers.map((player, idx) => {
          return <BlockSub
            key={player}
            id={player}
            can_add={true}
          />
        })}
        </tbody>
      </table>
    </div>
  )
}

export default BlockMembers