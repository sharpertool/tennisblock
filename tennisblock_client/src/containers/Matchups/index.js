import { connect } from 'react-redux'
import React, { Component } from 'react'
import { Row, Col, Button } from 'reactstrap'
import { withRouter } from 'react-router-dom'
import HeaderDate from '~/components/ui/Header/Date'
import { selectors, actions } from '~/Schedule/modules'
import MatchReview from '~/containers/MatchReview'


import styles from './styles.local.scss'

class Matchups extends Component {
  componentDidMount() {
    const { match, getBlockPlayers } = this.props
    const { params } = match
    if(match) {
      getBlockPlayers(params.id)
    }
  }

  calculateMatchups = () => {
    const { match, calculateMatchups } = this.props
    calculateMatchups(match.params.id)
  }

  render() {
    const { blockplayers, match, guyOptions, galOptions, changes } = this.props
    return(
      <div className="matches">
        <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id} />
        <Row className="mb-4">
          <Col className="d-flex justify-content-between" xs={3}>
            <Button color="danger"
                    onClick={this.calculateMatchups}>
              Calculate Matchups
            </Button>
          </Col>
        </Row>
        <Row>
        </Row>
        <Row>
          <MatchReview/>
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

const mapDispatchToProps = ({
  //getBlockPlayers: (val) => ({type: 'FU', payload: val}),
  //calculateMatchups: (val) => ({type: 'FU', payload: val}),
  getBlockPlayers: actions.getBlockPlayers,
  calculateMatchups: actions.calculateMatchups,
})

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(Matchups))
