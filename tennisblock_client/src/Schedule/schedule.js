import React from 'react'
import Proptypes from 'prop-types'
import {Provider} from 'react-redux'

import Schedule from '~/containers/Schedule'

const matchreview = ({store}) => {
  return (
    <Provider store={store}>
      <Schedule/>
    </Provider>)
}

matchreview.propTypes = {
}


export default Schedule
