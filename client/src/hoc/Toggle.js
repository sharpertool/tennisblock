import React, { Component } from 'react'

const Toggle = (WrappedComponent) => {
  return class extends Component {
    state = {
      isOpen: false
    }
    toggle = (e) => {
      this.setState({ isOpen: !this.state.isOpen })
    }
    render() {
      const { props } = this
      const { isOpen } = this.state
      return (
        <WrappedComponent isOpen={isOpen} onToggle={this.toggle} {...props} />
      )
    }
  }
}

export default Toggle