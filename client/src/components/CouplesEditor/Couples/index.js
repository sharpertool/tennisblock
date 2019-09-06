import React, {useEffect, useState} from 'react'
import styled from 'styled-components'

const CouplesDiv = styled.div`

    display: grid;
    grid-template-columns: auto;
    grid-template-rows: 40px auto;
    grid-auto-flow: row;
    grid-row-gap: 10px;

    grid-template-areas:
      "heading"
      "body"
    ;

    width: 100%;
    padding: 5px;
    margin: 2px;
    border: 1px solid #894fe6;
`

const CoupleGrid = styled.div`
    display: grid;
    grid-template-columns: 2fr 2fr 2fr 1fr 1fr 1fr;
    grid-row-gap: 2px;

`
const Header = styled(CoupleGrid)`
    grid-area: heading;
    border-bottom: 2px solid greenyellow;
`

const Body = styled(CoupleGrid)`
    grid-area: body;
`

import Couple from '../Couple'

const Couples = (props) => {
  
  const {
    couples,
    div_class,
    onCoupleNameChange,
    onCoupleFulltimeChange,
    onCoupleSinglesChange,
    onCoupleRemove,
  } = props
  
  return (
    <div className={div_class}>
      <CouplesDiv>
        <Header>
          <div style={{}}>Name</div>
          <div>Guy</div>
          <div>Girl</div>
          <div>Fulltime</div>
          <div>As Singles</div>
          <div>Remove</div>
        </Header>
        <Body>
          {couples.map((couple, idx) => {
            return (
              <Couple
                {...couple}
                onNameChange={(e) => onCoupleNameChange(e, idx)}
                onFulltimeChange={(e) => onCoupleFulltimeChange(e, idx)}
                onSinglesChange={(e) => onCoupleSinglesChange(e, idx)}
                onRemove={() => onCoupleRemove(idx)}
              />
            )
          })}
        </Body>
      </CouplesDiv>
    </div>
  )
}

export default Couples
