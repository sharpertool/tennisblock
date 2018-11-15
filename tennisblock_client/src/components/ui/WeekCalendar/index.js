import PropTypes from 'prop-types'
import React, { Fragment } from 'react'
import { Row } from 'reactstrap'
import Tiles from '~/components/ui/Tiles'
import { Link } from 'react-router-dom'

import styles from './styles.local.scss'

const weekcalendar = (props) => (
  <Fragment>
    <h2 className={styles.header}>
      <i className="fa fa-calendar" aria-hidden="true"></i> {new Date().getFullYear()} <Link to="/schedule"><i className="fa fa-pencil"></i></Link>
    </h2>
    <Row className="px-3">
      <Tiles dates={props.dates} classes={props.classes} />
    </Row>
  </Fragment>
)


weekcalendar.propTypes = {
  dates: PropTypes.array.isRequired
}

export default weekcalendar 