import React, { Component } from 'react'
import { types } from '~/ImageEditor/modules/Modal'

class XoomButton extends Component {
    handleZoom(e) {
        const { dispatch, dom_id } = this.props
        dispatch({ type: types.ZOOM_OPEN, dom_id })
    }
    render() {
        const { props, handleZoom } = this
        return(
            <a href="javascript:void(0)"
                onClick={handleZoom.bind(this)}
                className="card-link">
                <i className="fa fa-search-plus"></i>
            </a>
        )
    }
}


export default XoomButton
