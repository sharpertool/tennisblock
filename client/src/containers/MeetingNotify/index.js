import chunk from 'lodash/chunk'
import {connect} from 'react-redux'
import React, {useEffect} from 'react'
import HeaderDate from '~/components/ui/Header/Date'
import {Row, Col, Button, Input} from 'reactstrap'
import {withRouter} from 'react-router-dom'
import ActionButtons from './ActionButtons'
import styled from 'styled-components'
import Couples from './Couples'

const ErrorDiv = styled.div`
  color: red;
`

import {actions, selectors} from '~/redux-page'

import styles from './styles.local.scss'

const MeetingNotify = props => {
  
  const {match, message,
    updateMessage, getBlockPlayers,
    sendNotification,
    errors
  } = props
  
  useEffect(() => {
    // Get initial data
    console.log(match)
    getBlockPlayers({date: match.params.id})
  }, [])
  
  return (
    <div className="matches">
      <HeaderDate
        title="Fun Stuff"
        classNames="mb-4"
        link={`/schedule/${match.params.id}`} date={match.params.id}/>
        <ActionButtons sendNotification={() => sendNotification({message: message})}/>
      {errors.length > 0 ?
        <ErrorDiv>
          <h3>Errors:</h3>
          <ul>
            {errors.map((e,i) => {
              return (
                <li key={i}>{e}</li>
              )
            })}
          </ul>
        </ErrorDiv>
        : null
      }
      <Row className="mb-12">
        <Col className="d-flex justify-content-between">
        </Col>
      </Row>
      <Row>
        <Col md={12}>
          <Couples couples={props.couples}/>
        </Col>
      </Row>
      <Row>
          <textarea
            value={message}
            onChange={(e) => updateMessage(e.target.value)}
          >
          </textarea>
      </Row>
    </div>
  )
}

const mapStateToProps = (state) => {
  return {
    couples: selectors.getCouples(state),
    message: selectors.notify_message(state),
    errors: selectors.notify_errors(state),
  }
}

const mapDispatchToProps = {
  updateMessage: actions.scheduleNotifyMsgUpdate,
  getBlockPlayers: actions.getBlockPlayers,
  sendNotification: actions.scheduleNotify,
}

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingNotify))
