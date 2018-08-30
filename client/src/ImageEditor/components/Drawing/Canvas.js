import React, { Component } from 'react'
import { types } from '~/ImageEditor/modules/Drawing'
import { connect } from 'react-redux'
import { store } from '~/ImageEditor/provider/Client'
import Line from './Line'
import map from 'lodash/map'


class Canvas extends Component {
    handleMouseDown(e) {
        e.preventDefault()
        const { Drawing: { initialized }, dom_id, dispatch } = this.props
        if(initialized) {
            dispatch({ type: types.IS_DRAWING, dom_id })
        }

    }
    handleMouseMove(e) {
        e.preventDefault()
        const { dom_id, dispatch, Drawing } = this.props
        const clientRect = e.currentTarget.getBoundingClientRect()
        const x = e.clientX - clientRect.left
        const y = e.clientY - clientRect.top

        if(Drawing[`drawing-${dom_id}`].isDrawing) {
            const { enabled } = Drawing[`drawing-${dom_id}`]
            if(enabled) {
                const path = { x, y }
                const { active_color } = Drawing[`drawing-${dom_id}`]
                dispatch({ type: types.START, path, dom_id, stroke: active_color })
            }

        }

    }
    handleMouseUp(e) {
        e.preventDefault()
        const { dom_id, dispatch } = this.props
        dispatch({ type: types.END, dom_id })
    }

    render() {
        const {
            props,
            handleMouseUp,
            handleMouseMove,
            handleMouseDown
        } = this

        const { dom_id, Drawing, Drawing: { initialized } } = props

        if(initialized && Drawing[`drawing-${dom_id}`]) {

            const { paths, image } = Drawing[`drawing-${dom_id}`]
            return[
                <svg key={0}
                    id={`canvas-${dom_id}`}
                    ref={'canvas'}
                    className="canvas"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlnsXlink="http://www.w3.org/1999/xlink"
                    onMouseDown={this.handleMouseDown.bind(this)}
                    onMouseMove={this.handleMouseMove.bind(this)}
                    onMouseUp={this.handleMouseUp.bind(this)}
                    ref="canvas">
                    <image xlinkHref={image} width="100%" />
                    <g>
                        {paths.map((v, k) => {
                            const { path, stroke } = v
                            return(<Line key={k} stroke={stroke} paths={path} />)
                        })}
                    </g>
                </svg>
            ]

        }

        return null

    }
}

export default Canvas
