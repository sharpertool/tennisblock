import React, { Component } from 'react'
import { types } from '~/ImageEditor/modules/Drawing'

class EraseAll extends Component {
    handleErase(e) {
        const { dom_id, dispatch } = this.props
        dispatch({
            type: types.ERASE_ALL,
            dom_id
        })
    }
    render() {
        const { props, handleErase } = this
        const { Drawing } = props
        const { active_color, palette_colors } = Drawing
        return(
            <div className="eraser color-options mx-2">
                <a href="javascript:void(0)"
                    className={`p-2`}
                    onClick={handleErase.bind(this)}>
                    <i className="fa fa-trash" aria-hidden="true"></i>
                </a>
            </div>
        )
    }
}

export default EraseAll
