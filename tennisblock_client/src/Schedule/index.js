import React from 'react'
import {render} from 'react-dom'

// Build the Store stuff
import store from '~/Schedule/modules/store'
import ScheduleProvider from '~/Schedule/provider'
import './index.scss'

export default ({ target }) => {
  const element = document.getElementById(target)

  render(
    <ScheduleProvider store={store}/>,
    element,
  )
}
