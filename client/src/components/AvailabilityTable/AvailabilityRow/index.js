import React, {useRef, useEffect} from 'react'

const AvailabilityRow = ({
                           availability,
                           even,
                           availabilityChanged,
                         }) => {
  
  const {name, isavail, scheduled, played, nplayed, nscheduled} = availability
  
  const onAvailChanged = (idx) => {
    availabilityChanged({
      id: availability.id,
      mtgidx: idx,
      isavail: !isavail[idx]
    })
  }
  
  return (
    <tr className={even ? 'even' : 'odd'}>
      <td>{name}</td>
      {isavail.map((avail, idx) => {
          let classes = ['avrow_item', 'item']
          const is_scheduled = scheduled[idx]
          const did_play = played[idx]
          if (is_scheduled) {
            classes.push('scheduled')
          }
          if (did_play) {
            classes.push('played')
          }
          return (
            <td
              key={idx}
              className={classes.join(' ')}
            >
              <input type="checkbox"
                     className={classes.join(' ')}
                     checked={avail}
                     onChange={() => onAvailChanged(idx)}
              />
            </td>
          )
        }
      )
      }
      
      <td>
        {nplayed}
      </td>
      <td>
        {nscheduled}
      </td>
    
    </tr>
  )
}

AvailabilityRow.default_props = {}

AvailabilityRow.propTypes = {}

export default AvailabilityRow