import React, {useRef, useEffect} from 'react'

const MembersRow = ({
                           member,
                           even,
                           onBlockmemberChange
                         }) => {
  
  const {
    id, first, last, gender, ntrp, microntrp, email, phone, blockmember
  } = member
  
  const onMemberChange = (idx) => {
    onBlockmemberChange({
      id: availability.id,
      mtgidx: idx,
      isavail: !isavail[idx]
    })
  }
  
  return (
    <tr className={even ? 'even' : 'odd'}>
      <td>{first}</td>
      <td>{last}</td>
      <td>{gender}</td>
      <td>{ntrp}</td>
      <td>{microntrp}</td>
      <td>{email}</td>
      <td>{phone}</td>
      <td>{blockmember ? 'true' : 'false'}</td>
      <td><button>Edit</button></td>
    </tr>
  )
}

MembersRow.default_props = {}

MembersRow.propTypes = {}

export default MembersRow