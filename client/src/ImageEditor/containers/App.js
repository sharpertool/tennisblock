import { connect } from 'react-redux'
import Zoom from '~/ImageEditor/components/Zoom'
import DownloadModal from '~/ImageEditor/components/Download'
import ExpandButton from '~/ImageEditor/components/ImageControls/Expand'
import React, { Component, Children, cloneElement } from 'react'
import jsPDF from 'jspdf'
import { types } from '~/ImageEditor/modules/Modal'

class App extends Component {
    download (format, e) {
        const { dom_id } = this.props

        const svg = document.getElementById(`canvas-${dom_id}`)
        const svgData = new XMLSerializer().serializeToString(svg)
        const canvas = document.createElement('canvas')
        const svg_dim = svg.getBoundingClientRect()

        canvas.width = svg_dim.width
        canvas.height = svg_dim.height

        const ctx = canvas.getContext('2d')
        ctx.fillStyle = 'white'
        ctx.fillRect(0, 0, canvas.width, canvas.height)
        const svg_string = 'data:image/svg+xml,' + encodeURIComponent(svgData)

        let img = new Image()
        img.style.width = '100%'
        img.style.height = '100%'
        img.style.display = 'block'
        img.src = svg_string

        img.onload = () => {
            ctx.drawImage(img, 0, 0)
            switch (format) {
                case 'pdf':
                    this.downloadAsPDF(canvas)
                    break;
                case 'jpeg':
                    this.downloadAsImage(canvas, format)
                    break;
                case 'png':
                    this.downloadAsImage(canvas, format)
                    break;
            }
        }
    }

    downloadAsImage (canvas, format) {
        const { dom_id, dispatch } = this.props

        let link = document.createElement('a')
        link.href = canvas.toDataURL(`image/${format}`)
        link.download = `exported_drawing.${format}`
        link.style.display = 'none'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)

        dispatch({ type: types.DOWNLOAD_TOGGLE, dom_id })
    }

    downloadAsPDF (canvas) {
        const { dom_id, dispatch } = this.props

        let pdf = new jsPDF({
            orientation: 'portrait',
            unit: 'mm',
            format: 'a4'
        })
        pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, 205, 205)
        pdf.save('exported_drawing.pdf')

        dispatch({ type: types.DOWNLOAD_TOGGLE, dom_id })
    }

    render() {
        const { Modal, dom_id, dispatch, image } = this.props

        return(
            <div className="app-container">
                <ExpandButton {...this.props} />
                {Children.map(this.props.children, (child) => {
                    return cloneElement(child, { ...this.props })
                })}
                <Zoom dispatch={dispatch} dom_id={dom_id} modal={Modal[`drawing-zoom-${dom_id}`]}>
                    <img src={image} style={{ width: '100%' }}/>
                </Zoom>
                <DownloadModal dispatch={dispatch} dom_id={dom_id} modal={Modal[`drawing-download-${dom_id}`]}>
                    <div className="row">
                        <div className="col">
                            <button type="button" className="btn btn-primary btn-block" onClick={this.download.bind(this, 'pdf')}>PDF</button>
                        </div>
                        <div className="col">
                            <button type="button" className="btn btn-primary btn-block" onClick={this.download.bind(this, 'png')}>PNG</button>
                        </div>
                        <div className="col">
                            <button type="button" className="btn btn-primary btn-block" onClick={this.download.bind(this, 'jpeg')}>JPEG</button>
                        </div>
                    </div>
                </DownloadModal>
            </div>)
    }
}

export default connect(
    state => {
        return state
    },
    dispatch => { return { dispatch } }
)(App)
