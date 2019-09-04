import React from 'react'
import Responsive from 'react-responsive'

/**
 * This is straight out of the docs.
 * If I were to use this more than this one time, I'd move this to a
 * common file elsewhere.
 *
 */
export const Desktop = props => <Responsive
  {...props} minWidth={992}/>
export const Tablet = props => <Responsive
  {...props} minWidth={768} maxWidth={991}/>
export const Mobile = props => <Responsive
  {...props} maxWidth={767}/>
export const Default = props => <Responsive
  {...props} minWidth={768}/>
