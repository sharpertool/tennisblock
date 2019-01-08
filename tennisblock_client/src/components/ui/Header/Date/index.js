import React from 'react'
import { Link } from 'react-router-dom'

import {LocalDate} from '~/utils'
import styles from './styles.local.scss'

const headerDate = ({ link, date, classNames }) => (
  <h2 className={`${styles.header} ${classNames}`}>
    <Link to={link}>
      <i className="fa fa-calendar" aria-hidden="true"></i>
        &nbsp;
        {LocalDate(date).getFullYear()}
        &nbsp;| &nbsp;
        {LocalDate(date).toLocaleString('en-us',
          { month: 'long', day: '2-digit' })}
    </Link>
  </h2>
)


export default headerDate
