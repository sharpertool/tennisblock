import React from 'react'
import styled from 'styled-components'

import classes from './styles.scss'

const StyledP = styled.p`
  color: blue;
  background-color: lightgray;
`

const widget = () => {
  return (
    <div className={classes.Widget}>
      <h1>{'I am a widget'}</h1>
      <p>Just a test component.</p>
      <StyledP>Ah, this works for HMR... nice.</StyledP>
    </div>
  )
}

export default widget
