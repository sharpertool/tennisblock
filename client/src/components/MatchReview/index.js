import React from 'react'
import classes from './styles.local.scss'

import Match from '~/components/Match'

const MatchReview = (props) => {
  
  const {play_schedule, recalculateMatch, match} = props

  const date = match.params.id
  
  const schedule = play_schedule || []
  const matches = schedule.map((m, i) => {
      return (
        <Match key={i}
               idx={i + 1}
               courts={[...m]}
               date={date}
               onRecalculate={recalculateMatch}
        />
        )
    })
  
  return (
    <>
      <div className="col">
        <h3>
          React Play Schedule
        </h3>
      </div>
      
      {matches}
    </>
  )
}

export default MatchReview