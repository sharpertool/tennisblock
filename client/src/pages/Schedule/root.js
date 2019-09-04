import React from 'react'
import ReactDOM from 'react-dom'
import {Provider} from 'react-redux'
import { BrowserRouter as Router, browserHistory } from 'react-router-dom'

import App from '~/containers/App'
import Routes from './routes'

const root = ({store, elements}) => {
  
  return (
    <Provider store={store}>
      <Router history={browserHistory}>
        <App>
          <Routes/>
        </App>
      </Router>
    </Provider>)
}

export default root
