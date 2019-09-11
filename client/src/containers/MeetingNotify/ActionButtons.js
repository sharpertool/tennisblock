import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Button } from 'reactstrap'

const ActionButtons = props => {

  const { sendNotification } = props

  return (
    <>
      <Button
        className='col-3'
        color="danger"
        onClick={sendNotification}>
        Send Notifications
      </Button>
    </>
  )
}

ActionButtons.propTypes = {
  sendNotification: PropTypes.func.isRequired,
}

export default ActionButtons
