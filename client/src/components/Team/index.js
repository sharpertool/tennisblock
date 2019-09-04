import React from 'react'
import PropTypes from 'prop-types'

const team = (props) => {
  const {
    f: {name: gal, ntrp: galn, untrp: galu},
    m: {name: guy, ntrp: guyn, untrp: guyu}
    } = props

  return (
    <div className="col-6">
      <div className="col-12">
        {gal} ({galu})
      </div>
      <div className="col-12 text-center">
        and
      </div>
      <div className="col-12">
        {guy} ({guyu})
      </div>
      <div className="col-12">
        {(galu+guyu).toFixed(1)}
      </div>
    </div>
  )
}

team.propTypes = {}

export default team
