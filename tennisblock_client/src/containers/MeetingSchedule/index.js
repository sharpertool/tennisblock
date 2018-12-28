import chunk from 'lodash/chunk'
import {connect} from 'react-redux'
import React, {Component} from 'react'
import {Row, Col, Button} from 'reactstrap'
import {withRouter} from 'react-router-dom'
import {getBlockPlayers, changeBlockPlayer, updateBlockPlayers} from '~/Schedule/modules/schedule/actions'
import SelectBox from '~/components/Form/Fields/SelectBox'
import HeaderDate from '~/components/ui/Header/Date'
import HLink from '~/components/ui/Header/Link'
import {selectors} from '~/Schedule/modules'

import styles from './styles.local.scss'

class MeetingSchedule extends Component {
  componentDidMount() {
    const {match, getBlockPlayers} = this.props
    const {params} = match
    if (match) {
      getBlockPlayers(params.id)
    }
  }
  
  handleUpdate = () => {
    const {blockplayers, match, updateBlockPlayers} = this.props
    updateBlockPlayers({
      couples: blockplayers.couples,
      date: match.params.id
    })
  }
  
  render() {
    const {
      blockplayers, match,
      guyOptions, galOptions, changes
    } = this.props
    
    const couples = blockplayers.couples ? blockplayers.couples : []
    
    const can_clear_schedule = blockplayers.couples
    const can_schedule = !can_clear_schedule
    
    return (
      <div className="matches">
        <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id}/>
        <Row className="mb-4">
          <Col className="d-flex justify-content-between" xs={3}>
            <Button
              disabled={!can_schedule}
              color="danger">
              Schedule
            </Button>
            <Button
              disabled={!can_clear_schedule}
              color="danger">
              Clear Schedule
            </Button>
            <Button color="danger"
                    disabled={!this.props.isEdited}
                    onClick={this.handleUpdate}>
              Update Schedule
            </Button>
          </Col>
        </Row>
        <Row>
          <Col md={12}>
            <Row>
              <Col xs={6}>
                <h3 className={styles.tableHeader}>Guys</h3>
              </Col>
              <Col xs={6}>
                <h3 className={styles.tableHeader}>Gals</h3>
              </Col>
            </Row>
            <Row>
              {couples.map((couple, index) => {
                  const {guy, gal} = couple
                  return (
                    <React.Fragment key={index}>
                      <Col xs={12} md={6}>
                        <SelectBox
                          defaultValue={{
                            label: guy.name,
                            value: guy.id,
                            gender: 'guy',
                            index,
                            player: guy
                          }}
                          onChange={this.props.changeBlockPlayer}
                          options={guyOptions && guyOptions[index]}
                          isChanged={changes[index].guy}
                        />
                      </Col>
                      <Col xs={12} md={6}>
                        <SelectBox
                          defaultValue={{
                            label: gal.name,
                            value: gal.id,
                            gender: 'gal',
                            index,
                            player: gal
                          }}
                          onChange={this.props.changeBlockPlayer}
                          options={galOptions && galOptions[index]}
                          isChanged={changes[index].gal}
                        />
                      </Col>
                    </React.Fragment>
                  )
                }
              )
              }
            </Row>
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
    guyOptions: selectors.getGuySubOptions(state),
    galOptions: selectors.getGalSubOptions(state),
    changes: selectors.changes(state)
  }
}

const mapDispatchToProps = {
  getBlockPlayers,
  changeBlockPlayer,
  updateBlockPlayers
}

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingSchedule))
