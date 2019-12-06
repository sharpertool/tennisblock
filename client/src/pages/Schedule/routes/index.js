import React from 'react'
import {Switch, Route, BrowserRouter as Router} from 'react-router-dom'

import ScheduleContainer from '~/containers/ScheduleContainer'

import MeetingSchedule from '~/components/MeetingSchedule/connected'
import BlockSchedule from '~/containers/BlockSchedule'
import MeetingNotify from '~/containers/MeetingNotify'
import MeetingMatchups from '~/components/MeetingMatchups/connected'
import ErrorBoundary from '~/components/errorboundary/error_boundary'

const routes = () => (
  <ScheduleContainer>
    <Switch>
      <Route exact path="/schedule/">
        <BlockSchedule/>
      </Route>
      <Route exact path="/schedule/:id">
        <ErrorBoundary>
          <MeetingSchedule/>
        </ErrorBoundary>
      </Route>
      <Route exact path="/schedule/:id/mixer">
        <MeetingMatchups/>
      </Route>
      <Route exact path="/schedule/:id/notify">
        <MeetingNotify/>
      </Route>
    </Switch>
  </ScheduleContainer>
)

export default routes
