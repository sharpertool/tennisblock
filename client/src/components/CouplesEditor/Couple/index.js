import React, {useEffect, useState} from 'react'
import classes from './styles.local.scss'

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
  
  return (
    <tr>
      <td>
        <input
          type='text'
          name='name'
          value={name}
          onChange={e => onNameChange(e)}
        />
      </td>
      <td>{guy.name}</td>
      <td>{girl.name}</td>
      <td>
        <input
          type='checkbox'
          checked={fulltime}
          onChange={(e) => onFulltimeChange(e)}
          name='fulltime'/>
      </td>
      <td>
        <input
          type='checkbox'
          checked={as_singles}
          onChange={(e) => onSinglesChange(e)}
          name='as_singles'/>
      </td>
      <td>
        <button onClick={onRemove}>Remove</button>
      </td>
    </tr>
  )
}

export default Couple
