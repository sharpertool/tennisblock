import React, { Component } from 'react'
import { types } from '~/ImageEditor/modules/Drawing'

class Editor extends Component {
    handleDropdown(e) {
        const { dom_id, Drawing } = this.props
        const { brush_tool_open, enabled } = Drawing[`drawing-${dom_id}`]
        this.props.dispatch({
            type: types.TYPE_SELECTED,
            drawing_type: 'brush',
            brush_tool_open: !brush_tool_open,
            enabled: !enabled,
            dom_id
        })
    }
    render() {
        const { handleDropdown, props } = this
        const { dom_id, Drawing, Drawing: { initialized } } = props

        if(initialized && Drawing[`drawing-${dom_id}`]) {
            const { active_color, brush_tool_open } = Drawing[`drawing-${dom_id}`]
            return(
                <a href="javascript:void(0)"
                    className={`card-link ${brush_tool_open ? 'active' : ''}`}
                    onClick={handleDropdown.bind(this)}>
                    <i className="fa fa-pencil" aria-hidden="true"></i>
                </a>
            )
        }
        return null

    }
}


export default Editor
