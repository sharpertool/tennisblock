import React, { Component } from 'react'
import { line, curveBasis } from 'd3-shape'

class Line extends Component {
    render() {
        const { paths, stroke } = this.props
        const _line = line().curve(curveBasis)

        const createLine = _line.x((d) => d.x).y((d) => d.y)
        
        return(
            <path style={{ stroke, strokeWidth: 3, fill: 'none' }} d={createLine(paths)} />
        )
    }
}

export default Line
