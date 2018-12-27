import {connect} from 'react-redux'
import React, {Component} from 'react'
import {Row, Col, Button} from 'reactstrap'
import {withRouter} from 'react-router-dom'
import HeaderDate from '~/components/ui/Header/Date'
import {selectors, actions} from '~/Schedule/modules'
import MatchReview from '~/containers/MatchReview'


import styles from './styles.local.scss'

class Matchups extends Component {
  constructor(props) {
    super(props)

    this.state = {
      iterations: 1,
      tries: 1
    }
    this.ref1 = React.createRef()
    this.ref2 = React.createRef()
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
    const {iterations, tries} = this.state
    calculateMatchups({
      date: match.params.id,
      iterations: Number.parseInt(iterations),
      tries: Number.parseInt(tries)
    })
  }

  render() {
    const {match, calcResults} = this.props
    let errors = <div className={styles.error_div}><p></p></div>
    if (calcResults.status == 'fail') {
      errors = <div><p className="text-warning">Error: {calcResults.error}</p></div>
    }
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
    calcResults: selectors.calcResult(state)
  }
}

const mapDispatchToProps = ({
  getBlockPlayers: actions.getBlockPlayers,
  calculateMatchups: actions.calculateMatchups,
})

export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(Matchups))
