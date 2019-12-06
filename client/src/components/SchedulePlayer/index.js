import React from 'react'
import PropTypes from 'prop-types'
import {Input} from 'reactstrap'
import styles from './styles.local.scss'

import VerifyButtons from './VerifyButtons'

const SchedulePlayer = (props) => {
  
  const {
    index,
    player,
    group,
    subs,
    altsubs,
    verifyPlayer,
    notifyPlayer,
    onBlockPlayerChanged,
    verifyCode,
  } = props
  
  const onSendVerify = (id) => {
    console.log(`Send verification to ${id}`)
    notifyPlayer({id: id})
  }
  
  const onManualVerify = (id) => {
    console.log(`Manually verify id ${id}`)
    verifyPlayer({id: id})
  }
  
  let className = ''
  
  switch (verifyCode) {
    case 'C':
      className = styles.verified
      break
    case 'R':
      className = styles.rejected
      break
    case 'A':
      className = styles.awaiting
      break
    default:
      className = ''
  }

  const onInputChange = (e) => {
    const new_id = parseInt(e.target.value)
    const packet = {
          group: group,
          index: index,
          value: new_id,
          new_id: new_id,
          previous: player.id
      }
    onBlockPlayerChanged(packet)
  }
  
  return (
    <div className="form-group">
      <Input
        type="select"
        className={className}
        value={player.id}
        onChange={onInputChange}
      >
        <option
          value={player.id}>
          {player.name}
        </option>
        <option
          value={-1}>
          {'---'}
        </option>
        {subs.map((s, i) => (
          <option
            value={s.id} key={i}>
            {s.name}
          </option>
        ))}
        <option
          value={-1}>
          {'---'}
        </option>
        {altsubs.map((s, i) => (
          <option
            value={s.id} key={100 + i}>
            {s.name}
          </option>
        ))}
      </Input>
      <VerifyButtons
        id={player.id}
        vcode={verifyCode}
        onSendVerify={onSendVerify}
        onManualVerify={onManualVerify}
      />
    </div>
  )
}

SchedulePlayer.propTypes = {
  player: PropTypes.object.isRequired,
  subs: PropTypes.array,
  altsubs: PropTypes.array,
  verifyStatus: PropTypes.object,
  onBlockPlayerChanged: PropTypes.func.isRequired,
}

export default SchedulePlayer
