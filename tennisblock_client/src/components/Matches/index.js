import chunk from 'lodash/chunk'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import { Row, Col, Button } from 'reactstrap'
import { getBlockPlayers, updateCouple } from '~/Schedule/modules/schedule/actions'
import SelectBox from '~/components/Form/Fields/SelectBox'
import HeaderDate from '~/components/ui/Header/Date'

import styles from './styles.local.scss'

class Matches extends Component {
  componentDidMount() {
    const { match, getBlockPlayers } = this.props
    const { params } = match
    if(match) {
      getBlockPlayers(params.id)
    }
  }
  render() {
    const { blockplayers, subs, match } = this.props
    const { galsubs, guysubs } = subs
    
    return(
      <div className="matches">
        <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id} />
        <Row className="mb-4">
          <Col className="d-flex justify-content-between" xs={3}>
            <Button color="danger">Schedule</Button>
            <Button color="danger">Clear Schedule</Button>
            <Button color="danger">Update Schedule</Button>
          </Col>
        </Row>
        <Row>
          <Col xs={3}>
            <Row>
              <Col xs={6}>
                <h3 className={styles.tableHeader}>Guys</h3>
              </Col>
              <Col xs={6}>
                <h3 className={styles.tableHeader}>Gals</h3>
              </Col>
            </Row>
            <Row>
              <Col xs={12} md={6}>
                {blockplayers.guys && blockplayers.guys.map((guy, index) => (
                  <SelectBox key={index} defaultValue={guy.id} onChange={this.props.updateCouple} options={guysubs} id={guy.id} label={guy.name} />                
                ))}
              </Col>
              <Col xs={12} md={6}>
                {blockplayers.gals && blockplayers.gals.map((gal, index) => (
                  <SelectBox key={index} defaultValue={gal.id} onChange={this.props.updateCouple} options={galsubs} id={gal.id} label={gal.name} />
                ))}
              </Col>
            </Row>
          </Col>
        </Row>
      </div>
    )
  }
}

const mapStateToProps = ({ schedule }) => {
  const { blockplayers, subs } = schedule
  return {
    blockplayers,
    subs
  }
}

const mapDispatchToProps = {
  getBlockPlayers,
  updateCouple
}



export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Matches)
