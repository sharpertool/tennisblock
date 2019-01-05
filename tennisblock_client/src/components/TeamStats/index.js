import React from 'react'
import PropTypes from 'prop-types'

import classes from './index.local.scss'

const teamstats = (props) => {
  const {teams} = props
  const spread = teams.map((t) => {
    const {f: {untrp: fu}, m: {untrp: fm}} = t
    return Math.abs(fu - fm)
  })
  const totals = teams.map((t) => {
    const {f: {untrp: fu}, m: {untrp: fm}} = t
    return fu + fm
  })

  const mainClass = ['row', 'TeamStats'].join(' ')

  const barWidth = Math.min(100, 100*(spread[0]+spread[1])/2)
  const gauge1 = Math.min(100, 66.6*spread[0]) + '%'
  const gauge2 = Math.min(100, 66.6*spread[1]) + '%'
  const gauge3 = Math.min(100, 100*(Math.abs(totals[0]-totals[1]))) + '%'
  const height = 45


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
          <svg width="100%" height="50">
            <g>
              <rect className="outer" width="100%" height={height}/>
              <rect
                className={[classes.GaugeRect, classes.GaugeRect1].join(' ')}
                transform={`translate(1,1)`}
                width={gauge1}
                height={height/3-2}/>
              <rect
                className={[classes.GaugeRect, classes.GaugeRect2].join(' ')}
                transform={`translate(1,${height/3})`}
                width={gauge2}
                height={height/3-2}/>
              <rect
                className={[classes.GaugeRect, classes.GaugeRect3].join(' ')}
                transform={`translate(1,${2*height/3})`}
                width={gauge3}
                height={height/3-2}/>
            </g>
          </svg>
        </div>
      </div>
    </div>
  )
}

teamstats.propTypes = {}

export default teamstats
