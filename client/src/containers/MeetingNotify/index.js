import chunk from 'lodash/chunk'
import {connect} from 'react-redux'
import React, {Component} from 'react'
import {Row, Col, Button, Input} from 'reactstrap'
import {withRouter} from 'react-router-dom'
import HeaderDate from '~/components/ui/Header/Date'
import HLink from '~/components/ui/Header/Link'
import ActionButtons from './ActionButtons'
import Couples from './Couples'

import {actions, selectors} from '~/redux-page'

import styles from './styles.local.scss'

class MeetingNotify extends Component {
  
  render() {
    const props = this.props
    const {match} = this.props
    
    return (
      <div className="matches">
        <HeaderDate
          title="Fun Stuff"
          classNames="mb-4"
          link={`/schedule/${match.params.id}`} date={match.params.id}/>
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
          <textarea>
          
          </textarea>
          
        </Row>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    couples: selectors.getCouples(state),
  }
}

const mapDispatchToProps = {
}

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingNotify))
