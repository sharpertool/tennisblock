import React, {useRef, useEffect} from 'react'

const AvailabilityHeader = ({blockdates, onScroll, scrollLeft}) => {

  const itemsRef = useRef(null);
  useEffect(() => {
    if (itemsRef.current) {
      itemsRef.current.scrollLeft = scrollLeft
    }
  }, [scrollLeft])
  
  return (
    <div className='heading gridrow'>
      <div className='heading_item name_col'>
        Player Name
      </div>
      
      <div className='items'
           onScroll={(e) => onScroll(e.target.scrollLeft)}
           ref={itemsRef}>
        {blockdates.map((bd, idx) => {
            let classes = ['item']
            if (bd.holdout) { classes.push('holdout')}
            if (bd.current) { classes.push('current')}
            const d = new Date(bd.date)
            const dstring = d.toLocaleDateString('en',
                  {month: 'short', day:'numeric'}
                  )
            return (
              <div
                className={classes.join(' ')}
                key={idx}>
                {dstring}
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

AvailabilityHeader.default_props = {}

AvailabilityHeader.propTypes = {}

export default AvailabilityHeader