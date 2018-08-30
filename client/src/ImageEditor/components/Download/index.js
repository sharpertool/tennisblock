import React, { Component } from 'react'
import { Modal, ModalHeader, ModalBody } from 'reactstrap'
import { types } from '~/ImageEditor/modules/Modal'

class Download extends Component {
    handleModal(e) {
        const { dispatch, dom_id } = this.props
        dispatch({ type: types.DOWNLOAD_TOGGLE, dom_id })
    }
    render() {
        const { handleModal, props } = this
        const { modal } = props
        if(modal) {
            const { isOpen } = modal
            return(
                <Modal className="download-modal" isOpen={isOpen} toggle={handleModal.bind(this)}>
                    <ModalHeader toggle={handleModal.bind(this)} className="datapages-modal-header" />
                    <ModalBody>
                        { this.props.children }
                    </ModalBody>
                </Modal>
            )
        }
        return null
    }
}

export default Download