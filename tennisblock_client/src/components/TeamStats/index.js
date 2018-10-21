import React from 'react'
import PropTypes from 'prop-types'

import classes from './index.local.scss'

const teamstats = (props) => {
  console.log('TeamStats Props:', props)
  const {teams} = props
  const spread = teams.map(t => {
    const {f: {untrp: fu}, m: {untrp: fm}} = t
    return Math.abs(fu - fm)
  })

  const mainClass = ['row', classes.TeamStats].join(' ')

  const barWidth = Math.min(100, 100*(spread[0]+spread[1])/2)


  return (
    <div className="col-12">
      <div className={mainClass}>
        <div className="col-6">
          {spread[0].toFixed(1)}
        </div>
        <div className="col-6">
          {spread[1].toFixed(1)}
        </div>
      </div>
      <div className={mainClass}>
        <div className="col">
          <svg width="100%" height="30">
            <g>
              <rect className={classes.outer} width="100%" height="30"/>
              <rect className={classes.gauge}
                  transform={`translate(1,1)`}
                    width={barWidth+'%'}
                    height="28"/>
            </g>
          </svg>
        </div>
      </div>
    </div>
  )
}

teamstats.propTypes = {}

export default teamstats
