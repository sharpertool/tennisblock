import PropTypes from 'prop-types'
import React from 'react'
import { Link } from 'react-router-dom'

import styles from './styles.local.scss'

const tiles = ({ dates }) => {
  return dates && dates.map(({ date }, index) =>
      <Link to={`/schedule/${date}`} key={index} className={`${styles.tile} col-xs-12 col-sm-6 col-md-3 col-lg-2 col-xl-2 pt-2`}>
          <div className={styles.tileMonth}>
            {new Date(date).toLocaleString('en-us', { month: "long" })}
          </div>
          <div className={styles.tileDay}>
            {new Date(date).toLocaleString('en-us', { day: "numeric" })}
          </div>
      </Link>)
}

tiles.propTypes = {
  dates: PropTypes.array.isRequired
}

export default tiles
