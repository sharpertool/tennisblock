import React from 'react'
import {connect} from 'react-redux'
import {selectors, actions} from '~/redux-page'

import Availability from './index'

const connectedComponent = ({
                              blockdates,
                              availability,
                              onPlayerAvailabilityChange,
                            }) => {
  return (
    <Availability
      blockdates={blockdates}
      availability={availability}
      availabilityChanged={onPlayerAvailabilityChange}
    />
  )
}

const mapStateToProps = (state) => {
  return {
    blockdates: selectors['availability:blockdates'](state),
    availability: selectors['availability:availability'](state),
  }
}

const mapDispatchToProps = {
  onPlayerAvailabilityChange: actions['availability:onPlayerAvailabilityChange'],
}

export default connect(mapStateToProps, mapDispatchToProps)(connectedComponent)
