import React from 'react'
import Proptypes from 'prop-types'
import {Provider} from 'react-redux'

import Schedule from '~/containers/Schedule'

const root = ({store}) => {
  return (
    <Provider store={store}>
      <Schedule/>
    </Provider>)
}

root.propTypes = {
}


export default root
