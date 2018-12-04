import chunk from 'lodash/chunk'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import { Row, Col, Button } from 'reactstrap'
import { getBlockPlayers, updateCouple } from '~/Schedule/modules/schedule/actions'
import SelectBox from '~/components/Form/Fields/SelectBox'
import HeaderDate from '~/components/ui/Header/Date'

import styles from './styles.local.scss'


const shapeOptions = (values, { gender, index, defaultOpt }) => {
  const options = values.reduce((acc, value, i) => {
    acc[i] = { label: value.name, value: value.id, gender, index, player: value }
    return acc
  }, [])

  return [
    {
      label: defaultOpt.name,
      value: defaultOpt.id,
      gender,
      index,
      player: defaultOpt
    },
    ...options
  ]
}

class Matches extends Component {
  componentDidMount() {
    const { match, getBlockPlayers } = this.props
    const { params } = match
    if(match) {
      getBlockPlayers(params.id)
    }
  }
  render() {
    const { blockplayers, subs, match, originalCouples } = this.props
    const { galsubs, guysubs } = subs

    return(
      <div className="matches">
        <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id} />
        <Row className="mb-4">
          <Col className="d-flex justify-content-between" xs={3}>
            <Button color="danger">Schedule</Button>
            <Button color="danger">Clear Schedule</Button>
            <Button color="danger">Update Schedule</Button>
            <Button color="danger" disabled={!this.props.coupleChanged}>Save Changes</Button>
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
              {blockplayers.couples && blockplayers.couples.map((couple, index) => {
                const { guy, gal } = couple
                console.log(originalCouples)
                return (
                  <React.Fragment key={index}>
                    <Col xs={12} md={6}>
                      <SelectBox
                        key={index}
                        defaultValue={{ label: guy.name, value: guy.id, gender: 'guy', index, player: guy }}
                        onChange={this.props.updateCouple}
                        options={guysubs && shapeOptions(guysubs, { defaultOpt: originalCouples[index].guy, gender: 'guy', index })}
                        isChanged={originalCouples[index] && originalCouples[index].guy.id !== guy.id }
                        />
                    </Col>
                    <Col xs={12} md={6}>
                      <SelectBox
                        key={index}
                        defaultValue={{ label: gal.name, value: gal.id, gender: 'gal', index, player: gal }}
                        onChange={this.props.updateCouple}
                        options={galsubs && shapeOptions(galsubs, { defaultOpt: originalCouples[index].gal, gender: 'gal', index })}
                        isChanged={originalCouples[index] && originalCouples[index].gal.id !== gal.id }
                        />
                    </Col>
                  </React.Fragment>
                )
              })}
            </Row>
          </Col>
        </Row>
      </div>
    )
  }
}

const isObjectEqual = (x, y) => {
  x = Object.assign({}, x)
  y = Object.assign({}, y)
  return JSON.stringify(x) === JSON.stringify(y)
}

const mapStateToProps = ({ schedule }) => {
  const { blockplayers, subs, originalCouples } = schedule
  return {
    blockplayers,
    subs,
    originalCouples,
    coupleChanged: !isObjectEqual(blockplayers.couples, originalCouples)
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
