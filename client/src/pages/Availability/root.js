import React from 'react'
import {Provider} from 'react-redux'

import AvailabilityTable from '~/components/AvailabilityReactTable/connected'

const root = ({store}) => {
  
  return (
    <Provider store={store}>
      <AvailabilityTable/>
    </Provider>)
}

export default root
