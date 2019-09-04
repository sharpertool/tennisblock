import React from 'react'
import { connect } from 'react-redux'
import WeekCalender from '~/components/ui/WeekCalendar'

const blockSchedule = ({ meeting_dates }) => {
  return meeting_dates && <WeekCalender dates={meeting_dates} />
}

const mapStateToProps = ({schedule}) => {
    return {
      meeting_dates: schedule.meeting_dates
    }
}

export default connect(
  mapStateToProps
)(blockSchedule)
