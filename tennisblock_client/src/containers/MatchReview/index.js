import React, {Component} from 'react'
import classes from './styles.local.scss'
import {connect} from 'react-redux'

import {selectors as gsel} from '~/Schedule/modules'
import {actions as t_actions} from '~/Schedule/modules/teams'

import Match from '~/components/Match'

class MatchReview extends Component {

  render() {
    const { play_schedule, match } = this.props

    let matches = null
    if (play_schedule) {
      matches = play_schedule.map((m, i) =>
      {return (<Match key={i} idx={i+1} courts={[...m]}/>)})

    }

    return (
      <React.Fragment>
        <div className="col">
          <h3>
            React Play Schedule
          </h3>
        </div>

        {matches}
      </React.Fragment>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    play_schedule: gsel.playSchedule(state)
  }
}

/**
 * Object with key/values for dispatch actions
 *
 * connect will bind these to disptch, but I don't know if that
 * will support actions with values.
 * @type {{clickOptions: toggleOptions}}
 */
const dispatchActions = {
}


export default connect(mapStateToProps, dispatchActions)(MatchReview)
