import React from 'react'
import { Switch , Route, BrowserRouter as Router } from 'react-router-dom'

import MeetingSchedule from '~/containers/MeetingSchedule'
import BlockSchedule from '~/containers/BlockSchedule'
import Schedule from '~/containers/Schedule'
import Matchups from '~/containers/Matchups'

const routes = () => (
    <Schedule>
      <Route exact path="/schedule/" component={BlockSchedule} />
      <Route exact path="/schedule/:id" component={MeetingSchedule} />
      <Route exact path="/schedule/:id/mixer" component={Matchups} />
    </Schedule>
)

export default routes
