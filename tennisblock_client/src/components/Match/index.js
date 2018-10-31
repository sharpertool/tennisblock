import React from 'react'
import PropTypes from 'prop-types'

import Court from '~/components/Court'

const match = (props) => {
  console.log('Match Props:', props)
  const {idx, courts} = props

  const courtRender = courts.map((court, idx) => {
    return (
      <Court key={idx} idx={idx+1} {...court}/>
    )
  })

  return (
    <div className="row">
      <div className="col-12">
          <h4>Match {props.idx}</h4>
      </div>
      {courtRender}
    </div>
  )
}

match.propTypes = {}

export default match
