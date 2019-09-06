import React from 'react'

const TargetItem = (props) => {
  
  
  const {
    player,
  } = props
  
  return (
    <div
    >
      {player ? `${player.first} ${player.last}` : ''}
    </div>
  )
}

export default TargetItem