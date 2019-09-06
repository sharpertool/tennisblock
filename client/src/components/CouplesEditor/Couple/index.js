import React, {useEffect, useState} from 'react'

const Couple = ({
                   name,
                   guy,
                   girl,
                   as_singles,
                   fulltime,
                   onNameChange,
                   onFulltimeChange,
                   onSinglesChange,
                   onRemove,
                 }) => {
  
  const pname = (p) => `${p.first} ${p.last}`
  
  return (
    <>
      <div>
        <input
          type='text'
          name='name'
          value={name}
          onChange={e => onNameChange(e)}
        />
      </div>
      <div>{pname(guy)}</div>
      <div>{pname(girl)}</div>
      <div>
        <input
          type='checkbox'
          checked={fulltime}
          onChange={(e) => onFulltimeChange(e)}
          name='fulltime'/>
      </div>
      <div>
        <input
          type='checkbox'
          checked={as_singles}
          onChange={(e) => onSinglesChange(e)}
          name='as_singles'/>
      </div>
      <div>
        <button onClick={onRemove}>Remove</button>
      </div>
    </>
  )
}

export default Couple
