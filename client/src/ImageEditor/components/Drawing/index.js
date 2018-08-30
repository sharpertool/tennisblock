import Canvas from './Canvas'
import React, { Component } from 'react'
import DrawingMenu from './Menu'
import BrushTool from './BrushTool'

class Drawing extends Component {

    render() {
        const { props } = this
        return(
            <div className="row">
                <div className="col">
                    <Canvas {...props} />
                    <DrawingMenu>
                        <BrushTool {...props} />
                    </DrawingMenu>
                </div>
            </div>
        )
    }
}

export default Drawing
