import EraseAll from './EraserAll'
import React, { Component } from 'react'
import { types } from '~/ImageEditor/modules/Drawing'
import { connect } from 'react-redux'

class BrushTool extends Component {
    handleColorChange(active_color, e) {
        const { dom_id, Drawing } = this.props
        e.preventDefault()
        this.props.dispatch({
            type: types.COLOR_SELECTED,
            active_color,
            dom_id
        })
    }
    render() {
        const { props, state, handleColorChange, handleDropdown } = this
        const { dom_id, Drawing, Drawing: { initialized, palette_colors } } = props

        if(initialized && Drawing[`drawing-${dom_id}`]) {
            const { active_color, brush_tool_open } = Drawing[`drawing-${dom_id}`]
            return(
                <div className="color-switcher">
                    {brush_tool_open ?
                        <div className="color-switcher-options d-flex justify-content-center align-items-center">
                            {palette_colors.map((v, k) =>
                                <div key={k}
                                    className={`color-options mx-2 ${v === active_color ? 'active' : ''}`}
                                    style={{ width: '20px', height: '20px', background: v, cursor: 'grab' }}
                                    onClick={handleColorChange.bind(this, v)}>
                                </div>
                            )}
                            <EraseAll {...props} />
                        </div> : null}
                </div>
            )
        }
        return null
    }
}

export default BrushTool
