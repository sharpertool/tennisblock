import React, { Component } from 'react'
import PropTypes from 'prop-types'
import { Button } from 'reactstrap'
import ConfirmDialog from '~/components/ui/ConfirmDialog'
import styles from './styles.local.scss'

class ActionButtons extends Component {
  constructor(props) {
    super(props)

    this.state = {
      confirm: false,
      type: null
    }
  }

  toggleConfirm = (type) => {
    this.setState({
      confirm: !this.state.confirm,
      type: type
    })
  }
  
  onConfirm = () => {
    const {type} = this.state
    if (type == 'reschedule') {
      this.props.onReSchedule()
    } else if (type == 'clearschedule') {
      this.props.onClear()
    }
    this.setState({confirm: false, type:null})
  }

  handleUpdate = () => {
    this.props.onUpdate()
  }

  render() {
    const { canClear, canSchedule, canUpdate } = this.props

    return (
      <React.Fragment>
        <ConfirmDialog
          isOpen={this.state.confirm}
          toggle={this.toggleConfirm}
          onConfirm={this.onConfirm}
        >
          You are about to clear the schedule. Do you wish to continue?
        </ConfirmDialog>

        <Button
          disabled={!canSchedule}
          onClick={() => this.toggleConfirm('reschedule')}
          color="danger">
          Schedule
        </Button>

        <Button
          disabled={!canClear}
          onClick={() => this.toggleConfirm('clearschedule')}
          color="danger">
          Clear Schedule
        </Button>

        <Button
          color="danger"
          disabled={!canUpdate}
          onClick={this.handleUpdate}>
          Update Schedule
        </Button>
      </React.Fragment>
    )
  }
}

ActionButtons.propTypes = {
  canClear: PropTypes.bool.isRequired,
  canReSchedule: PropTypes.bool.isRequired,
  canUpdate: PropTypes.bool.isRequired,
  
  onReSchedule: PropTypes.func.isRequired,
  onUpdate: PropTypes.func.isRequired,
  onClear: PropTypes.func.isRequired,
}

export default ActionButtons
