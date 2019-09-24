import React, {useRef, useEffect} from 'react'

const BlockSub = ({
                    id,
                    player,
                    even,
                    can_add,
                    toggleBlockSub,
                  }) => {
  
  const {
    user: {first_name: first},
    user: {last_name: last},
    gender,
    ntrp,
    microntrp,
    email,
    phone,
  } = player
  
  return (
    <tr className={even ? 'even' : 'odd'}>
      <td>{first}</td>
      <td>{last}</td>
      <td>{gender}</td>
      <td>{ntrp}</td>
      <td>{microntrp}</td>
      <td>{email}</td>
      <td>{phone}</td>
      <td>
        <button className={'btn btn-primary'}
          onClick={() => toggleBlockSub({id: id})}>
          {can_add ? 'Add as Sub' : 'Remove as Sub'}
        </button>
      </td>
    </tr>
  )
}

BlockSub.default_props = {}

BlockSub.propTypes = {}

export default BlockSub