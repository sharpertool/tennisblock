import React from 'react'
import { Switch, Route } from 'react-router-dom'

import Matches from '~/components/Matches'
import BlockSchedule from '~/containers/BlockSchedule'

const routes = () => (
  <Switch>
    <Route exact path="/schedule" component={BlockSchedule} />
    <Route exact path="/schedule/:id" component={Matches} />
  </Switch>
)
 


export default routes
