import React, {useEffect, useState} from 'react'
import classes from './styles.local.scss'

import Couple from '../Couple'

const Couples = (props) => {
  
  const {
    couples,
    onCoupleNameChange,
    onCoupleFulltimeChange,
    onCoupleSinglesChange,
    onCoupleRemove,
  } = props
  
  return (
    <div className={classes.couples}>
      <table>
        <tr>
          <th>Name</th>
          <th>Guy</th>
          <th>Girl</th>
          <th>Fulltime</th>
          <th>As Singles</th>
          <th>Remove</th>
        </tr>
        
        {couples.map((couple, idx) => {
          return (
            <Couple
              {...couple}
              onNameChange={(e) => onCoupleNameChange(e, idx)}
              onFulltimeChange={(e) => onCoupleFulltimeChange(e, idx)}
              onSinglesChange={(e) => onCoupleSinglesChange(e, idx)}
              onRemove={() => onCoupleRemove(idx)}
              />
          )
        })}
      </table>
    </div>
  )
}

export default Couples
