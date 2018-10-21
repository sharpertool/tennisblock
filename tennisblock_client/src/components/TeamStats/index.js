import React from 'react'
import PropTypes from 'prop-types'

import classes from './index.local.scss'

const teamstats = (props) => {
  console.log('TeamStats Props:', props)
  const {teams} = props
  const spread = teams.map(t => {
    const {f: {untrp: fu}, m: {untrp: fm}} = t
    return Math.abs(fu - fm).toFixed(1)
  })

  const mainClass = ['row', classes.TeamStats].join(' ')


  return (
    <div className="col-12">
      <div className={mainClass}>
        <div className="col-6">
          {spread[0]}
        </div>
        <div className="col-6">
          {spread[1]}
        </div>
      </div>
      <div className={mainClass}>
        <div className="col">
          <svg width="250" height="30">
            <g>
              <rect width="250" height="30"/>
            </g>
          </svg>
        </div>
      </div>
    </div>
  )
}

teamstats.propTypes = {}

export default teamstats
