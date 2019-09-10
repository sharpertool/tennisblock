import React from 'react'
import { Switch , Route, BrowserRouter as Router } from 'react-router-dom'

import ScheduleContainer from '~/containers/ScheduleContainer'

import MeetingSchedule from '~/containers/MeetingSchedule'
import BlockSchedule from '~/containers/BlockSchedule'
import MeetingMatchups from '~/containers/MeetingMatchups'
import MeetingNotify from '~/containers/MeetingNotify'

const routes = () => (
    <ScheduleContainer>
      <Route exact path="/schedule/" component={BlockSchedule} />
      <Route exact path="/schedule/:id" component={MeetingSchedule} />
      <Route exact path="/schedule/:id/mixer" component={MeetingMatchups} />
      <Route exact path="/schedule/:id/notify" component={MeetingNotify} />
    </ScheduleContainer>
)

export default routes
