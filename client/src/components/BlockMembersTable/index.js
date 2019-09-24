import React from 'react'

import MembersHeader from './MembersHeader'
import MemberRow from './MembersRow'

const BlockMembers = ({
                        blockmembers,
            onBlockmemberChange,
                      }) => {
  return (
    <div id='members' className={'members'}>
      <table className={'member_list table'}>
        <MembersHeader
        />
        <tbody>
          {blockmembers.map((member, idx) => {
            return (<MemberRow
              key={idx}
              even={idx%2==0}
              member={member}
              onBlockmemberChange={onBlockmemberChange}
            />)
          })}
        </tbody>
      </table>
    </div>
  )
}

export default BlockMembers