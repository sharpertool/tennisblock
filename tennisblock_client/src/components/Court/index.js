import React from 'react'
import PropTypes from 'prop-types'

import Team from '~/components/Team'
import TeamStats from '~/components/TeamStats'

const court = (props) => {
  console.log('Court Props:', props)
  const {idx, team1, team2} = props

  return (
    <div className="col-lg col-md-6 col-xs-12">
      <p>Court {idx}</p>
      <div className="row">
        <Team {...team1}/>
        <Team {...team2}/>
        <TeamStats teams={[team1,team2]}/>
      </div>
    </div>
  )
}

court.propTypes = {}

export default court
