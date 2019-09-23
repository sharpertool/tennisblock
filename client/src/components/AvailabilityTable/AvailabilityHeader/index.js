import React, {useRef, useEffect} from 'react'

const AvailabilityHeader = ({blockdates}) => {
  
  return (
    <thead>
    <tr className='even'>
      <th>
        Player Name
      </th>
      
      {blockdates.map((bd, idx) => {
          let classes = []
          if (bd.holdout) {
            classes.push('holdout')
          } else {
            classes.push('play')
          }
          if (bd.current) {
            classes.push('current')
          }
          const d = new Date(bd.date)
          const dstring = d.toLocaleDateString('en',
            {month: 'short', day: 'numeric'}
          )
          return (
            <th
              className={classes.join(' ')}
              key={idx}>
              {dstring}
            </th>
          )
        }
      )
      }
      
      <th className='heading_item played_col'>
        # Played
      </th>
      <th className='heading_item schedule_col'>
        # Schedule
      </th>
    
    </tr>
    </thead>
  )
}

AvailabilityHeader.default_props = {}

AvailabilityHeader.propTypes = {}

export default AvailabilityHeader