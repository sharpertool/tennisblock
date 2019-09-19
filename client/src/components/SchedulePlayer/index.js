import React, {Component} from 'react'
import PropTypes from 'prop-types'
import {Input} from 'reactstrap'
import SelectBox from '~/components/Form/Fields/SelectBox'
import styles from './styles.local.scss'

const SchedulePlayer = (props) => {
  
  const {
    index,
    player,
    group,
    subs,
    altsubs,
    verifyStatus,
    verifyPlayer,
    notifyPlayer,
    onPlayerChanged,
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
  const vcode = verifyStatus[player.id]
  
  switch (vcode) {
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
  
  const buttons = (vcode, id) => {
    switch (vcode) {
      case 'N':
        return (
          <>
            <button onClick={() => onSendVerify(id)}>Send Verification Request</button>
            <button onClick={() => onManualVerify(id)}>Verify</button>
          </>
        
        )
      case 'A':
        return (
          <>
            <button onClick={() => onSendVerify(id)}>re-send Verification Request</button>
            <button onClick={() => onManualVerify(id)}>Verify</button>
          </>
        )
      default:
        return null
    }
  }
  
  return (
    <div className="form-group">
      <Input
        type="select"
        className={className}
        value={player.id}
        onChange={(e) => onPlayerChanged({
          group: group,
          index: index,
          value: parseInt(e.target.value),
          previous: player.id
        })}
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
      {buttons(vcode, player.id)}
    </div>
  )
}

SchedulePlayer.propTypes = {
  player: PropTypes.object.isRequired,
  subs: PropTypes.array,
  altsubs: PropTypes.array,
  verifyStatus: PropTypes.object,
  onPlayerChanged: PropTypes.func,
}

export default SchedulePlayer
