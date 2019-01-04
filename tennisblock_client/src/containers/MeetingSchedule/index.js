import chunk from 'lodash/chunk'
import {connect} from 'react-redux'
import React, {Component} from 'react'
import { Row, Col, Button, Input } from 'reactstrap'
import {withRouter} from 'react-router-dom'
import HeaderDate from '~/components/ui/Header/Date'
import HLink from '~/components/ui/Header/Link'
import ActionButtons from './ActionButtons'
import Couples from './Couples'

import {actions, selectors} from '~/Schedule'

import styles from './styles.local.scss'

class MeetingSchedule extends Component {
  componentDidMount() {
    const {match, getBlockPlayers} = this.props
    const {params} = match
    if (match) {
      getBlockPlayers(params.id)
    }
  }

  render() {
    const props = this.props
    const {match} = this.props

    return (
      <div className="matches">
        <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id}/>
        <Row className="mb-4">
          <Col className="d-flex justify-content-between" xs={3}>
            <ActionButtons
              canClear={props.canClearSchedule}
              canReSchedule={props.canReSchedule}
              canUpdate={props.canUpdateSchedule}
              onReSchedule={props.onReSchedule}
              onClear={props.clearSchedule}
              onUpdate={props.updateBlockPlayers}
            />
          </Col>
        </Row>
        <Row>
          <Col md={12}>
            <Couples
              onPlayerChanged={props.onPlayerChanged}
              couples={props.couples}
              guySubs={props.guySubs}
              galSubs={props.galSubs}
              />
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
    guySubs: selectors.getGuySubs(state),
    galSubs: selectors.getGalSubs(state),
    couples: selectors.getCouples(state),
    canClearSchedule: selectors.canClearSchedule(state),
    canReSchedule: selectors.canReSchedule(state),
    canUpdateSchedule: selectors.isScheduleChanged(state),
    isScheduleChanged: selectors.isScheduleChanged(state),
  }
}

const mapDispatchToProps = {
  getBlockPlayers: actions.getBlockPlayers,
  onPlayerChanged: actions.onPlayerChanged,
  updateBlockPlayers: actions.updateBlockPlayers,
  clearSchedule: actions.clearSchedule,
  onReSchedule: actions.reSchedule,
}

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingSchedule))
