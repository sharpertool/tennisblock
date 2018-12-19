import React from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import { BrowserRouter as Router, browserHistory } from 'react-router-dom'

import App from '~/containers/App'
import Routes from '~/Schedule/routes'

import ScheduleLayout from '~/containers/Schedule'

const scheduleProvider = ({ store }) => (
  <Provider store={store}>
    <Router history={browserHistory}>
      <App>
        <Routes />
      </App>
    </Router>
  </Provider>
)

scheduleProvider.propTypes = {
  store: PropTypes.object,
}

export default scheduleProvider
