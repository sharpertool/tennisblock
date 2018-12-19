import React from 'react'
import { Switch , Route, BrowserRouter as Router } from 'react-router-dom'

import Matches from '~/components/Matches'
import BlockSchedule from '~/containers/BlockSchedule'
import Schedule from '~/containers/Schedule'

const routes = () => (
    <Schedule>
      <Route exact path="/schedule/" component={BlockSchedule} />
      <Route exact path="/schedule/:id" component={Matches} />
    </Schedule>
)

export default routes
