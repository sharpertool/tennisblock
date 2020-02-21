import React from 'react'
import PropTypes from 'prop-types'

import Court from '~/components/Court'
import {Button, Col} from 'reactstrap';

const match = (props) => {
  const {courts} = props

  const rebuild = () => {
    console.log(`Rebuilding match ${props.idx}`)
    const {onRecalculate} = props
    onRecalculate({
      date: props.date,
      setnumber: props.idx,
    })
  }

  const courtRender = courts.map((court, idx) => {
    return (
      <Court key={idx} idx={idx+1} {...court}/>
    )
  })

  return (
    <div className="row">
      <div className="col-12">
          <h4>Match {props.idx}</h4>
          <Button color="danger"
                 onClick={rebuild} >
            Rebuild This Match
          </Button>
      </div>
      {courtRender}
    </div>
  )
}

match.propTypes = {}

export default match
