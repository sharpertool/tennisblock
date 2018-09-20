import React from 'react'

import classes from './styles.scss'

const widget = (props) => {
  return (
    <div className={classes.Widget}>
      <h1>I am a widget</h1>
      <h3>I'm here also</h3>
    </div>
  )
}

export default widget