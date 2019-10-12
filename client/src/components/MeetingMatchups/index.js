import React, {useState, useRef, useEffect} from 'react'

import {Row, Col, Button} from 'reactstrap'
import HeaderDate from '~/components/ui/Header/Date'
import MatchReview from '~/components/MatchReview/connected'


import styles from './styles.local.scss'

const MeetingMatchups = (props) => {
  
  const {fetchCurrentSchedule} = props
  useEffect(() => {
    fetchCurrentSchedule({date: match.params.id})
  }, [])
  
  const [state, setState] = useState({
    iterations: 25,
    tries: 35,
    fpartner: 1.0,
    fteam: 1.5,
  })
  
  const ref1 = useRef()
  const ref2 = useRef()
  const ref3 = useRef()
  const ref4 = useRef()
  
  const onChange = (e) => {
    const name = e.target.name
    const value = e.target.value
    setState((state) => {
      let newState = {...state}
      newState[name] = value
      console.dir(newState)
      return newState
    })
  }
  
  const handleFocus = (e) => {
    e.preventDefault()
    e.target.select()
  }
  
  const handleDoubleClick = (e) => {
    e.preventDefault()
    e.target.select()
  }
  
  const calculateMatchups = () => {
    const {match, calculateMatchups} = props
    const {iterations, tries, fpartner, fteam} = state
    calculateMatchups({
      date: match.params.id,
      iterations: Number.parseInt(iterations),
      tries: Number.parseInt(tries),
      fpartner: Number.parseFloat(fpartner),
      fteam: Number.parseFloat(fteam),
    })
  }
  
  const {match, calcResults, validPlaySchedule} = props
  let errors = <div className={styles.error_div}><p></p></div>
  if (calcResults.status == 'fail') {
    errors = <div><p className="text-warning">Error: {calcResults.error}</p></div>
  }
  
  const download = validPlaySchedule ?
    <a href={`/api/blocksheet/${match.params.id}/`}
       target="_blank"
       role="button"
       className="btn btn-danger pull-right"
    >
      Download Blocksheet
    </a> : null
  
  return (
    <div className={['matches', styles.matches].join(' ')}>
      <HeaderDate classNames="mb-4" link={`/schedule/${match.params.id}`} date={match.params.id}/>
      <Row className="mb-4">
        <Col className="d-flex justify-content-between" xs={3}>
          Iterations:
          <input name="iterations"
                 ref={ref1}
            //onFocus={handleFocus}
                 onChange={onChange}
                 onDoubleClick={handleDoubleClick}
                 type="number"
                 min="1" max="1000"
                 value={state.iterations}/>
          Tries:
          <input name="tries"
                 ref={ref2}
            //onFocus={handleFocus}
                 onChange={onChange}
                 onDoubleClick={handleDoubleClick}
                 type="number"
                 min="1" max="100"
                 value={state.tries}/>
          Fpartner:
          <input name="fpartner"
                 ref={ref3}
                 onChange={onChange}
                 onDoubleClick={handleDoubleClick}
                 type="number"
                 step="0.1"
                 min="1" max="10"
                 value={state.fpartner}/>
          Fteam:
          <input name="fteam"
                 ref={ref4}
                 onChange={onChange}
                 onDoubleClick={handleDoubleClick}
                 type="number"
                 step="0.1"
                 min="1" max="10"
                 value={state.fteam}/>
        </Col>
      </Row>
      <Row>
        {errors}
      </Row>
      <Row>
        <Col className="d-flex justify-content-left">
          <Button color="danger"
                  onClick={calculateMatchups}>
            Calculate Matchups
          </Button>
          {download}
        </Col>
      </Row>
      <Row>
        <MatchReview {...props}/>
      </Row>
    </div>
  )
}

export default MeetingMatchups