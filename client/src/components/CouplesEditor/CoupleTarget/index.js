import React from "react"

import TargetItem from './TargetItem'
import classes from './styles.local.scss'

const CoupleTarget = (props) => {
  
  const {
    guy,
    girl,
    onDragOver,
    onDragEnter,
    onDrop,
  } = props
  
  return (
    <div
      className={classes.target}
        onDragOver={onDragOver}
        onDragEnter={onDragEnter}
        onDrop={onDrop}
    >
      <TargetItem
        player={guy}
        />
      <TargetItem
        player={girl}/>
    </div>
  
  )
}

export default CoupleTarget