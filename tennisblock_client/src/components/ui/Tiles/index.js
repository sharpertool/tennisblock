import PropTypes from 'prop-types'
import React from 'react'
import { Link } from 'react-router-dom'

import styles from './styles.local.scss'

const tiles = ({ dates }) => {
  return dates && dates.map(({ date }, index) =>
    <div key={index} className={`${styles.tile} col-xs-12 col-sm-6 col-md-3 col-lg-2 col-xl-2 pt-2`}>
      <Link to={`/${date}`} className={styles.tileEdit}>
        <i className="fa fa-pencil" aria-hidden="true"></i>
      </Link>
      <div className={styles.tileMonth}>
        {new Date(date).toLocaleString('en-us', { month: "long" })}
      </div>
      <div className={styles.tileDay}>
        {new Date(date).getDate()}
      </div>
    </div>)
}

tiles.propTypes = {
  dates: PropTypes.array.isRequired
}

export default tiles