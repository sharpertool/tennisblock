import React from 'react'
import PropTypes from 'prop-types'

const team = (props) => {
  console.log('Team Props:', props)
  const {
    f: {name: gal, ntrp: galn, untrp: galu},
    m: {name: guy, ntrp: guyn, untrp: guyu}
    } = props

  return (
    <React.Fragment>
    <div className="col-5">
      {gal} ({galu})
    </div>
    <div className="col-1">
      and
    </div>
    <div className="col-5">
      {guy} ({guyu})
    </div>
    <div className="col-1">
      {galu+guyu}
    </div>
    </React.Fragment>
  )
}

team.propTypes = {}

export default team
