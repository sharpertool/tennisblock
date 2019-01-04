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
    const {
      blockplayers, match,
      guyOptions, galOptions, changes
    } = this.props

    return (
      <div className="matches">
        <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id}/>
        <Row className="mb-4">
          <Col className="d-flex justify-content-between" xs={3}>
            <ActionButtons {...this.props} />
          </Col>
        </Row>
        <Row>
          <Col md={12}>
            <Couples {...this.props} />
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
    guySubs: selectors.getGuySubs(state),
    galSubs: selectors.getGalSubs(state),
    changes: selectors.changes(state),
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
