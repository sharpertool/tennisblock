import React from 'react'
import PropTypes from 'prop-types'

import classes from './index.local.scss'

const teamstats = (props) => {
  const {teams} = props
  const spread = teams.map((t) => {
    const {f: {untrp: fu}, m: {untrp: mu}} = t
    return Math.abs(fu - mu)
  })
  const totals = teams.map((t) => {
    const {f: {untrp: fu}, m: {untrp: mu}} = t
    return fu + mu
  })
  
  const teamdiff = totals[1] - totals[0]
  
  const mainClass = ['row', 'TeamStats'].join(' ')
  
  const barWidth = Math.min(100, 100 * (spread[0] + spread[1]) / 2)
  const gauge1 = Math.min(100, 66.6 * spread[0]) + '%'
  const gauge2 = Math.min(100, 66.6 * spread[1]) + '%'
  const gauge3 = Math.min(100, 100 * (Math.abs(totals[0] - totals[1]))) + '%'
  const n = 4
  const height = 25 * n
  
  const viewport = {width: 100, height: 100}
  const rectheight = viewport.height / n - 2
  
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
          <svg xmlns="http://www.w3.org/2000/svg"
               width={'300px'} height={height + 15}
               viewBox={'0 0 100 100'}
               preserveAspectRatio={'none'}
          >
            <rect className={classes.OuterRect}
                  x='0' y='0'
                  width={'100'} height={'100'}
            />
            <rect
              className={[classes.GaugeRect, classes.GaugeRect1].join(' ')}
              transform={'translate(1,1)'}
              width={gauge1}
              height={rectheight}/>
            <rect
              className={[classes.GaugeRect, classes.GaugeRect2].join(' ')}
              transform={`translate(1,${100 / n})`}
              width={gauge2}
              height={rectheight}/>
            <rect
              className={[classes.GaugeRect, classes.GaugeRect3].join(' ')}
              transform={`translate(1,${2 * 100 / n})`}
              width={gauge3}
              height={rectheight}/>
            <rect
              className={[classes.GaugeRect, classes.GaugeRect4].join(' ')}
              y={3*100/n}
              x={teamdiff<0 ? 50+(teamdiff*100/2) : 50}
              width={Math.abs(teamdiff*100/2)}
              height={rectheight}/>
            <rect className={'centerline'}
                  x={50} y={75}
                  width={1}
                  height={25}
                  />>
          </svg>
        </div>
      </div>
    </div>
  )
}

teamstats.propTypes = {}

export default teamstats
