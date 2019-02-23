import {connect} from 'react-redux'
import React, {Component} from 'react'
import {Row, Col, Button} from 'reactstrap'
import {withRouter} from 'react-router-dom'
import HeaderDate from '~/components/ui/Header/Date'
import {selectors, actions} from '~/Schedule/modules'
import MatchReview from '~/containers/MatchReview'


import styles from './styles.local.scss'

class MeetingMatchups extends Component {
  constructor(props) {
    super(props)

    this.state = {
      iterations: 1,
      tries: 1,
      fpartner: 1.0,
      fteam: 1.0,
    }
    this.ref1 = React.createRef()
    this.ref2 = React.createRef()
    this.ref3 = React.createRef()
    this.ref4 = React.createRef()
  }

  onChange = (e) => {
    this.setState({[e.target.name]: e.target.value})
  }

  handleFocus = (e) => {
    e.preventDefault()
    e.target.select()
  }

  calculateMatchups = () => {
    const {match, calculateMatchups} = this.props
    const {iterations, tries, fpartner, fteam} = this.state
    calculateMatchups({
      date: match.params.id,
      iterations: Number.parseInt(iterations),
      tries: Number.parseInt(tries),
      fpartner: Number.parseFloat(fpartner),
      fteam: Number.parseFloat(fteam),
    })
  }

  render() {
    const {match, calcResults, validPlaySchedule} = this.props
    let errors = <div className={styles.error_div}><p></p></div>
    if (calcResults.status == 'fail') {
      errors = <div><p className="text-warning">Error: {calcResults.error}</p></div>
    }
    
    const download = validPlaySchedule ?
              <a href={`/api/blocksheet/${match.params.id}`}
                target="_blank"
                 role="button"
                className="btn btn-danger pull-right"
              >
                Download Blocksheet
              </a> : null
    
    return (
      <div className={["matches", styles.matches].join(' ')}>
        <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id}/>
        <Row className="mb-4">
          <Col className="d-flex justify-content-between" xs={3}>
            Iterations:
            <input name="iterations"
                   ref={this.ref1}
                   //onFocus={this.handleFocus}
                   onChange={this.onChange}
                   type="number"
                   min="1" max="1000"
                   value={this.state.iterations}/>
            Tries:
            <input name="tries"
                   ref={this.ref2}
                   //onFocus={this.handleFocus}
                   onChange={this.onChange}
                   type="number"
                   min="1" max="100"
                   value={this.state.tries}/>
            Fpartner:
            <input name="fpartner"
                   ref={this.ref3}
                   onChange={this.onChange}
                   type="number"
                   min="1" max="10"
                   value={this.state.fpartner}/>
            Fteam:
            <input name="fteam"
                   ref={this.ref4}
                   onChange={this.onChange}
                   type="number"
                   min="1" max="10"
                   value={this.state.fteam}/>
          </Col>
        </Row>
        <Row>
          {errors}
        </Row>
        <Row>
          <Col className="d-flex justify-content-left">
            <Button color="danger"
                    onClick={this.calculateMatchups}>
              Calculate Matchups
            </Button>
            {download}
          </Col>
        </Row>
        <Row>
          <MatchReview {...this.props}/>
        </Row>
      </div>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    calcResults: selectors.calcResult(state),
    validPlaySchedule: selectors.validPlaySchedule(state)
  }
}

const mapDispatchToProps = ({
  getBlockPlayers: actions.getBlockPlayers,
  calculateMatchups: actions.calculateMatchups,
})

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(MeetingMatchups))
