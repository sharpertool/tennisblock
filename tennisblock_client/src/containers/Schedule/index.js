import React, {Component} from 'react'
import classes from './styles.local.scss'
import {connect} from 'react-redux'

import {selectors as gsel} from 'Schedule/modules'
import {actions as t_actions} from 'Schedule/modules/teams'

class Schedule extends Component {

  render() {
    console.log('[Schedule]', this.props)
    const {play_schedule} = this.props
    console.log('Play Schedule:', play_schedule)

    return (
      <React.Fragment>
        <h3>Block Meetings</h3>
        <MeetingSelector/>
        <Meeting/>
      </React.Fragment>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    //play_schedule: gsel.playSchedule(state)
  }
}

/**
 * Object with key/values for displatch actions
 *
 * connect will bind these to disptch, but I don't know if that
 * will support actions with values.
 * @type {{clickOptions: toggleOptions}}
 */
const dispatchActions = {
}


export default connect(mapStateToProps, dispatchActions)(Schedule)
