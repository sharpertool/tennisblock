import React from 'react'
import {render} from 'react-dom'

// Build the Store stuff
import mkStore from './modules'
import ScheduleProvider from './provider'
import './index.scss'

import { selectors } from './modules'
export { selectors }

import { actions } from './modules'
export { actions }

const store = mkStore()

export default ({ target }) => {
  const element = document.getElementById(target)

  render(
    <ScheduleProvider store={store}/>,
    element,
  )
}
