import React, {useRef, useEffect} from 'react'

const AvailabilityRow = ({availability, onScroll, scrollLeft}) => {
  
  const itemsRef = useRef(null);
  useEffect(() => {
    if (itemsRef.current) {
      itemsRef.current.scrollLeft = scrollLeft
    }
  }, [scrollLeft])
  
  const {name, isavail, scheduled} = availability
  return (
    <div className='avrow gridrow'>
      <div className='avrow_item name_col'>
        {name}
      </div>
      
      <div className='items'
           onScroll={(e) => onScroll(e.target.scrollLeft)}
           ref={itemsRef}
      >
        {isavail.map((avail, idx) => {
            let classes = ['avrow_item', 'item']
            const is_scheduled = scheduled[idx]
            if (is_scheduled) {
              classes.push('scheduled')
            }
            return (
              <div
                key={idx}
                className={classes.join(' ')}
              >
                <input type="checkbox"
                       className={classes.join(' ')}
                       value={avail}
                />
              </div>
            )
          }
        )
        }
      </div>
      
      <div className='heading_item played_col'>
        # Played
      </div>
      <div className='heading_item schedule_col'>
        # Schedule
      </div>
    
    </div>
  )
}

AvailabilityRow.default_props = {}

AvailabilityRow.propTypes = {}

export default AvailabilityRow