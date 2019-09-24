import React, {Component} from 'react'
import PropTypes from 'prop-types'
import {Input} from 'reactstrap'
import SelectBox from '~/components/Form/Fields/SelectBox'
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
    onPlayerChanged,
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
  onPlayerChanged: PropTypes.func,
}

export default SchedulePlayer
