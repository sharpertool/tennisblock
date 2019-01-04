import React, { Component } from 'react'
import { Modal, ModalHeader, ModalBody, ModalFooter, Button } from 'reactstrap'
import propTypes from './prop-types'

class ConfirmDialog extends Component {
  render() {
    return (
      <Modal isOpen={this.props.isOpen}>
        <ModalHeader>Confirmation Message</ModalHeader>
        <ModalBody>
          {this.props.children}
        </ModalBody>
        <ModalFooter>
          <Button color="danger" onClick={this.props.onConfirm}>Yes</Button>
          <Button color="secondary" onClick={this.props.toggle}>Cancel</Button>
        </ModalFooter>
      </Modal>
    )
  }
}

ConfirmDialog.propTypes = propTypes

export default ConfirmDialog
