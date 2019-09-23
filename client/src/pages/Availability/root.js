import React from 'react'
import {Provider} from 'react-redux'

import Availability from '~/components/Availability/connected'
import AvailabilityTable from '~/components/AvailabilityTable/connected'

const root = ({store}) => {
  
  return (
    <Provider store={store}>
      <AvailabilityTable/>
    </Provider>)
}

export default root
