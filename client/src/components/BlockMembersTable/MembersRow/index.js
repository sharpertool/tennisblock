import React, {useRef, useEffect} from 'react'

const Member = ({
                  member,
                  player,
                  even,
                  onBlockmemberChange
                }) => {
  
  const {
    first, last,
    gender,
    ntrp,
    microntrp,
    email,
    phone,
    blockmember,
    fulltime
  } = member

  const {
    user: {first_name: fn},
    user: {last_name: ln},
  } = player
  
  const onMemberChange = (idx) => {
    onBlockmemberChange({
      id: availability.id,
      mtgidx: idx,
      isavail: !isavail[idx]
    })
  }

  const ftstyle = {
    backgroundColor: fulltime ? '#6699ff' : '#ffffcc'
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
      <td style={ftstyle}>{fulltime ? 'true' : 'false'}</td>
      <td>
      </td>
    </tr>
  )
}

Member.default_props = {}

Member.propTypes = {}

export default Member