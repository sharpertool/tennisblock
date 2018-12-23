import React from 'react'
import {render} from 'react-dom'

// Build the Store stuff
import mkStore from './modules'
import ScheduleProvider from './provider'
import './index.scss'

import {actions as act} from './modules/actions'
export const actions = act

const store = mkStore()

export default ({ target }) => {
  const element = document.getElementById(target)

  render(
    <ScheduleProvider store={store}/>,
    element,
  )
}
