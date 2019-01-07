import React, { Component } from 'react'
import { withRouter, matchPath } from 'react-router'
import { Link } from 'react-router-dom'
import { selectors } from '~/Schedule/modules'
import classes from './styles.local.scss'

const matchRoute = (pathname) => {
  return matchPath(pathname, { path: '/schedule/:id' })
}

class Breadcrumb extends Component {
  render() {
    const match = matchRoute(this.props.history.location.pathname)
    return (
      <nav>
        <ol className="breadcrumb">
          <li className={['breadcrumb-item', !match ? 'active' : ''].join(' ')}>
            {!match ? 'Schedule' : <Link to="/schedule/">Schedule</Link>}
          </li>
          {match && match.params.id ?
            <li className="breadcrumb-item active">{ match.params.id }</li> : null}
        </ol>
      </nav>
    )
  }
}

export default withRouter(Breadcrumb)
