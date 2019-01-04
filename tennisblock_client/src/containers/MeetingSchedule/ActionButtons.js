import React, { Component } from 'react'
import { Button } from 'reactstrap'
import ConfirmDialog from '~/components/ui/ConfirmDialog'
import styles from './styles.local.scss'

class ActionButtons extends Component {
  constructor(props) {
    super(props)

    this.state = {
      confirm: false
    }
  }

  toggleConfirm = () => {
    this.setState({
      confirm: !this.state.confirm
    })
  }

  handleUpdate = () => {
    const {blockplayers, match, updateBlockPlayers} = this.props
    updateBlockPlayers({
      couples: blockplayers.couples,
      date: match.params.id
    })
  }

  handleClear = () => {
    const {clearSchedule, match} = this.props
    clearSchedule({date: match.params.id})
    this.setState({confirm: false})
  }

  render() {
    const { blockplayers } = this.props

    const is_schedule_empty = blockplayers.couples.every(c => {
      return c.guy.name == '----' && c.gal.name == '----'
    })
    const can_clear_schedule = !is_schedule_empty
    const can_schedule = !can_clear_schedule

    return (
      <React.Fragment>
        <ConfirmDialog
          isOpen={this.state.confirm}
          toggle={this.toggleConfirm}
          onConfirm={this.handleClear}
        >
          You are about to clear the schedule. Do you wish to continue?
        </ConfirmDialog>

        <Button
          disabled={!can_schedule}
          color="danger">
          Schedule
        </Button>

        <Button
          disabled={!can_clear_schedule}
          onClick={this.toggleConfirm}
          color="danger">
          Clear Schedule
        </Button>

        <Button
          color="danger"
          disabled={!this.props.isEdited}
          onClick={this.handleUpdate}>
          Update Schedule
        </Button>
      </React.Fragment>
    )
  }
}

export default ActionButtons
