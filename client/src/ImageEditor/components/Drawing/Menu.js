import React, { Component } from 'react'

class Menu extends Component {
    render() {
        return(
            <div className="drawing-menu d-flex justify-content-center align-items-center">
                {this.props.children}
            </div>
        )
    }
}


export default Menu
