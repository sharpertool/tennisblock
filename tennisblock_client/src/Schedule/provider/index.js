import React from 'react'
import PropTypes from 'prop-types'
import { Provider } from 'react-redux'
import { BrowserRouter as Router } from 'react-router-dom'

import App from '~/containers/App'
import Routes from '~/Schedule/routes'

const scheduleProvider = ({ store }) => (
  <Provider store={store}>
    <App>
      <Router>
        <Routes />
      </Router>
    </App>
  </Provider>
)

scheduleProvider.propTypes = {
  store: PropTypes.object,
}

export default scheduleProvider
