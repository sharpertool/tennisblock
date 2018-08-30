import { connect } from 'react-redux'
import React, { cloneElement, Children, Component } from 'react'

class App extends Component {
    render() {
        return(
            <div className="sidebar-container">
                {Children.map(this.props.children, (child) => {
                    return cloneElement(child, { ...this.props })
                })}
            </div>
        )
    }
}

export default connect(
    state => {
        return state
    },
    dispatch => { return { dispatch } }
)(App)
