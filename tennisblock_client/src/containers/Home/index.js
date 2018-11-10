import React from 'react'
import { render } from 'react-dom'
import Home from './home'

export default (homepage) => {
    render(<Home/>, document.getElementById(homepage))
}