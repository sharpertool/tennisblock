import React, {useEffect} from 'react'
import {Row, Col, Button, Input} from 'reactstrap'
import HeaderDate from '~/components/ui/Header/Date'
import HLink from '~/components/ui/Header/Link'
import ActionButtons from './ActionButtons'

import ScheduledCouples from '~/components/ScheduledCouples/connected'

const MeetingSchedule = (props) => {
  
  const {match, getBlockPlayers, onDateChange} = props
  
  useEffect(() => {
    if (match) {
      const {params} = match
      onDateChange({date: params.id})
      getBlockPlayers({date: params.id})
    }
    
  }, [match])
  
  
  return (
    <div className="matches">
      <HeaderDate classNames="mb-4"
                  link={`/schedule/${match.params.id}`}
                  date={match.params.id}/>
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

export default MeetingSchedule