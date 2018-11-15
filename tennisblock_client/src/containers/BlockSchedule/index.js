import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'
import WeekCalender from '~/components/ui/WeekCalendar'

const blockSchedule = ({ blockdates }) => {
  return blockdates && <WeekCalender dates={blockdates} />
}

const mapStateToProps = ({ schedule }) => ({ blockdates: schedule.blockdates })

export default connect(
  mapStateToProps
)(blockSchedule)
