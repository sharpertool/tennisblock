import React, {useState} from 'react'

import AvailabilityHeader from './AvailabilityHeader'
import AvailabilityRow from './AvailabilityRow'

const Availability = ({
                        blockdates,
                        availability,
                      }) => {
  
  const [scrollLeft, setScroll] = useState(0)
  const onScroll = (val) => {
    setScroll(val)
  }
  
  return (
    <div className={'availability'}>
      <AvailabilityHeader
        blockdates={blockdates}
        onScroll={onScroll}
        scrollLeft={scrollLeft}
      />
      {availability.map((av, idx) => {
        return (<AvailabilityRow
          key={idx}
          availability={av}
          onScroll={onScroll}
          scrollLeft={scrollLeft}
        />)
      })}
    </div>
  )
}

export default Availability