import React, { Component } from 'react'
import { types } from '~/ImageEditor/modules/Modal'

class Download extends Component {
    handleDownload (e) {
        const { dispatch, dom_id } = this.props
        dispatch({ type: types.DOWNLOAD_OPEN, dom_id })
    }
    render () {
        const { handleDownload } = this
        return (
            <a href="javascript:void(0)"
                className="card-link" onClick={handleDownload.bind(this)}>
                <i className="fa fa-download" aria-hidden="true"></i>
            </a>
        )
    }
}

export default Download
