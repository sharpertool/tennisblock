import chunk from 'lodash/chunk'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import { Row, Col } from 'reactstrap'
import { getBlockPlayers } from '~/Schedule/modules/teams/actions'
import SelectBox from '~/components/Form/Fields/SelectBox'
import HeaderDate from '~/components/ui/Header/Date'
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
        <HeaderDate link={`/schedule/${match.params.id}`} date={match.params.id} />
        <Row>
          <Col xs={3}>
            <Row>
              <Col xs={6}>
                <h3>Gals</h3>
              </Col>
              <Col xs={6}>
                <h3>Guys</h3>
              </Col>
            </Row>
            {blockplayers && chunk(blockplayers.couples, 2).map((couples, index) => (
              <Row key={index}>
                {couples.map((couple, key) => (
                  <Col xs={6} key={key}>
                    <SelectBox options={galsubs} id={couple.gal.id} label={couple.gal.name} />
                    <SelectBox options={guysubs} id={couple.guy.id} label={couple.guy.name} />
                  </Col>
                ))}
              </Row>
            ))}
          </Col>
        </Row>
      </div>
    )
  }
}

const mapStateToProps = ({ teams }) => {
  const { blockplayers, subs } = teams
  return {
    blockplayers,
    subs
  }
}

const mapDispatchToProps = {
  getBlockPlayers
}



export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Matches)
