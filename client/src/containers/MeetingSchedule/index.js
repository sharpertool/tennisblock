import chunk from 'lodash/chunk'
import {connect} from 'react-redux'
import React, {Component, useEffect} from 'react'
import {Row, Col, Button, Input} from 'reactstrap'
import {withRouter} from 'react-router-dom'
import HeaderDate from '~/components/ui/Header/Date'
import HLink from '~/components/ui/Header/Link'
import ActionButtons from './ActionButtons'

import {actions, selectors} from '~/redux-page'

import ScheduledCouples from '~/components/ScheduledCouples/connected'

const MeetingSchedule = (props) =>  {

  const {match, getBlockPlayers} = props

  useEffect(() => {
    const {params} = match
    if (match) {
      getBlockPlayers({date: params.id})
    }
    
  }, [match])
  
  
  return (
    <div className="matches">
      <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id}/>
      <Row className="mb-12">
        <Col className="d-flex justify-content-between">
          <Row>
            <ActionButtons
              canClear={props.canClearSchedule}
              canReSchedule={props.canReSchedule}
              canUpdate={props.canUpdateSchedule}
              onReSchedule={props.onReSchedule}
              onClear={props.clearSchedule}
              onUpdate={props.updateBlockPlayers}
              onNotify={props.onNotify}
            />
          <HLink
            title="Notify"
            link={`/schedule/${match.params.id}/notify`}
            >
            </HLink>
          </Row>
        </Col>
      </Row>
      <Row>
        <Col md={12}>
          <ScheduledCouples
            couples={props.couples}
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

const mapStateToProps = (state) => {
  return {
    couples: selectors.getCouples(state),
    canClearSchedule: selectors.canClearSchedule(state),
    canReSchedule: selectors.canReSchedule(state),
    canUpdateSchedule: selectors.isScheduleChanged(state),
  }
}

const mapDispatchToProps = {
  getBlockPlayers: actions.getBlockPlayers,
  updateBlockPlayers: actions.updateBlockPlayers,
  clearSchedule: actions.clearSchedule,
  onReSchedule: actions.reSchedule,
  onNotify: actions.scheduleNotify,
}

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingSchedule))
