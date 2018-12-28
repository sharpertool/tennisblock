import React from 'react'
import { Switch , Route, BrowserRouter as Router } from 'react-router-dom'

import ScheduleContainer from '~/containers/ScheduleContainer'

import MeetingSchedule from '~/containers/MeetingSchedule'
import BlockSchedule from '~/containers/BlockSchedule'
import MeetingMatchups from '~/containers/Matchups'

const routes = () => (
    <ScheduleContainer>
      <Route exact path="/schedule/" component={BlockSchedule} />
      <Route exact path="/schedule/:id" component={MeetingSchedule} />
      <Route exact path="/schedule/:id/mixer" component={MeetingMatchups} />
    </ScheduleContainer>
)

export default routes
