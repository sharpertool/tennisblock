import React from 'react'
import { connect } from 'react-redux'
import { Link } from 'react-router-dom'

const blockSchedule = ({ blockdates }) => {
  return blockdates && blockdates.map((blockdate, index) => <Link to={`/${blockdate.date}`}><div key={index}>{blockdate.date}</div></Link>)
}

const mapStateToProps = ({ schedule }) => ({ blockdates: schedule.blockdates })

export default connect(
  mapStateToProps
)(blockSchedule)
