import React from 'react'
import PropTypes from 'prop-types'

const app = ({ children }) => (
  <div className="app">
    {children}
  </div>
)

app.propTypes = {
  children: PropTypes.node,
}

export default app
