import chunk from 'lodash/chunk'
import {connect} from 'react-redux'
import React, {Component} from 'react'
import {Row, Col, Button} from 'reactstrap'
import {withRouter} from 'react-router-dom'
import SelectBox from '~/components/Form/Fields/SelectBox'
import HeaderDate from '~/components/ui/Header/Date'
import HLink from '~/components/ui/Header/Link'
import ConfirmDialog from '~/components/ui/ConfirmDialog'

import {actions, selectors} from '~/Schedule'

import styles from './styles.local.scss'

class MeetingSchedule extends Component {
  constructor(props) {
    super(props)
    
    this.state = {
      confirm: false
    }
  }
  
  componentDidMount() {
    const {match, getBlockPlayers} = this.props
    const {params} = match
    if (match) {
      getBlockPlayers(params.id)
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
    const {
      blockplayers, match,
      guyOptions, galOptions, changes
    } = this.props
    
    const couples = blockplayers.couples ? blockplayers.couples : []
    
    const is_schedule_empty = blockplayers.couples.every(c => {
      return c.guy.name == '----' && c.gal.name == '----'
    })
    const can_clear_schedule = !is_schedule_empty
    const can_schedule = !can_clear_schedule
    
    return (
      <div className="matches">
        <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id}/>
        <Row className="mb-4">
          <Col className="d-flex justify-content-between" xs={3}>
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
            <Button color="danger"
                    disabled={!this.props.isEdited}
                    onClick={this.handleUpdate}>
              Update Schedule
            </Button>
          </Col>
        </Row>
        <Row>
          <Col md={12}>
            <Row>
              <Col xs={6}>
                <h3 className={styles.tableHeader}>Guys</h3>
              </Col>
              <Col xs={6}>
                <h3 className={styles.tableHeader}>Gals</h3>
              </Col>
            </Row>
            <Row>
              {couples.map((couple, index) => {
                  const {guy, gal} = couple
                  return (
                    <React.Fragment key={index}>
                      <Col xs={12} md={6}>
                        <SelectBox
                          defaultValue={{
                            label: guy.name,
                            value: guy.id,
                            gender: 'guy',
                            index,
                            player: guy
                          }}
                          onChange={this.props.changeBlockPlayer}
                          options={guyOptions && guyOptions[index]}
                          isChanged={changes[index].guy}
                        />
                      </Col>
                      <Col xs={12} md={6}>
                        <SelectBox
                          defaultValue={{
                            label: gal.name,
                            value: gal.id,
                            gender: 'gal',
                            index,
                            player: gal
                          }}
                          onChange={this.props.changeBlockPlayer}
                          options={galOptions && galOptions[index]}
                          isChanged={changes[index].gal}
                        />
                      </Col>
                    </React.Fragment>
                  )
                }
              )
              }
            </Row>
          </Col>
        </Row>
        <Row>
          <HLink
            title="Play Sheet"
            link={`/schedule/${match.params.id}/mixer`}/>
        </Row>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    blockplayers: selectors.getBlockPlayers(state),
    isEdited: selectors.isBlockPlayerEdited(state),
    guyOptions: selectors.getGuySubOptions(state),
    galOptions: selectors.getGalSubOptions(state),
    changes: selectors.changes(state)
  }
}

const mapDispatchToProps = {
  getBlockPlayers: actions.getBlockPlayers,
  changeBlockPlayer: actions.changeBlockPlayer,
  updateBlockPlayers: actions.updateBlockPlayers,
  clearSchedule: actions.clearSchedule
}

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingSchedule))
