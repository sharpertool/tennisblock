import React from 'react'
import { Link } from 'react-router-dom'

import styles from './styles.local.scss'

const elem = ({ title, link, classNames }) => (
  <h3 className={`${styles.header} ${classNames}`}>
    <Link to={link}>
      <i className="fa " aria-hidden="true"></i>
      {title}
    </Link>
  </h3>
)


export default elem