import React, {useRef, useEffect} from 'react'

const MembersHeader = () => {
  
  return (
    <thead>
    <tr className='even'>
      <th>
        First
      </th>
      <th>
        Last
      </th>
      <th className='heading_item played_col'>
        Gender
      </th>
      <th className='heading_item schedule_col'>
        NTRP
      </th>
      <th className='heading_item schedule_col'>
        uNTRP
      </th>
      <th className='heading_item schedule_col'>
        Email
      </th>
      <th className='heading_item schedule_col'>
        Phone
      </th>
      <th className='heading_item schedule_col'>
        Block Member?
      </th>
      <th className='heading_item schedule_col'>
        FullTime?
      </th>
      <th className='heading_item schedule_col'>
        Action
      </th>
    </tr>
    </thead>
  )
}

MembersHeader.default_props = {}

MembersHeader.propTypes = {}

export default MembersHeader