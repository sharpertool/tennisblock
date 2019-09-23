import React from 'react'

import AvailabilityHeader from './AvailabilityHeader'
import AvailabilityRow from './AvailabilityRow'

const Availability = ({
                        blockdates,
                        availability,
            availabilityChanged,
                      }) => {
  return (
    <div id='available' className={'availability'}>
      <table className={'member_list table'}>
        <AvailabilityHeader
          blockdates={blockdates}
        />
        <tbody>
          {availability.map((av, idx) => {
            return (<AvailabilityRow
              key={idx}
              even={idx%2==0}
              availability={av}
              availabilityChanged={availabilityChanged}
            />)
          })}
        </tbody>
      </table>
    </div>
  )
}

export default Availability