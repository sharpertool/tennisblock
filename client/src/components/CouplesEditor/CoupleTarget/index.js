import React from "react"
import styled from 'styled-components'

import TargetItem from './TargetItem'

const DropDiv = styled.div`
  height-min: 80px;
  background-color: lightcyan;
  //margin: 10px;
  padding: 10px;
`

const CoupleTarget = (props) => {
  
  const {
    grid_class,
    guy,
    girl,
    onDragOver,
    onDragEnter,
    onDrop,
  } = props
  
  const empty = !girl && !guy
  
  return (
    <DropDiv
      className={grid_class}
      onDragOver={onDragOver}
      onDragEnter={onDragEnter}
      onDrop={onDrop}
    >
      {empty ?
        <span>Drop a Guy or Girl Here</span>
        : <>
          <TargetItem
            player={guy}
          />
          <TargetItem
            player={girl}/>
          <span>Now drop the Partner Here</span>
        </>
      }
    </DropDiv>
  
  )
}

export default CoupleTarget