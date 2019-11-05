import PropTypes from 'prop-types'
import React from 'react'
import {Link} from 'react-router-dom'
import {LocalDate} from '~/utils'

import styles from './styles.local.scss'

const tiles = ({dates}) => {
  return dates && dates.map(({date, holdout}, index) => {
    const localdate = LocalDate(date)
    const linkClasses = [styles.tile, 'col-xs-12 col-sm-6 col-md-3 col-lg-2 col-xl-2 pt-2']
    if (holdout) {
      linkClasses.push(styles.holdout)
    }
    
    return (
      <Link to={`/schedule/${date}`} key={index}
            className={linkClasses.join(' ')}>
        <div className={styles.tileMonth}>
          {localdate.getMonth()+1}
        </div>
        <div className={styles.tileDay}>
          {localdate.getDate()}
        </div>
      </Link>
    )
  })
}

tiles.propTypes = {
  dates: PropTypes.array.isRequired
}

export default tiles
