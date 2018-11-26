import React from 'react'
import { Link } from 'react-router-dom'

import styles from './styles.local.scss'

const headerDate = ({ link, date }) => (
  <h2 className={styles.header}>
    <Link to={link}>
      <i className="fa fa-calendar" aria-hidden="true"></i>
        &nbsp;
        {new Date(date).getFullYear()}
        &nbsp;| &nbsp;
        {new Date(date).toLocaleString('en-us', { month: "long" })}&nbsp;
        {new Date(date).getDate()}
    </Link>
  </h2>
)


export default headerDate