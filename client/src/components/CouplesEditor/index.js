import React, {useEffect, useState} from 'react'
import classes from './styles.local.scss'

const CouplesEditor = (props) => {
  
  const [couples, setCouples] = useState([])
  const [couple, setCouple] = useState({guy: null, girl: null})
  const [_guys, setGuys] = useState([])
  const [_girls, setGirls] = useState([])
  const [dragObj, setDragObj]= useState(null)

  const {guys, girls} = props
  
  useEffect(() => {
    setCouples([])
    setGuys(guys)
    setGirls(girls)
  }, [guys, girls])
  
  
  const onDragStart = (e, obj) => {
    const sobj = JSON.stringify(obj)
    const dt = e.dataTransfer
    dt.setData('text/json', sobj)
    dt.setData('text/plain', obj.id)
    setDragObj(obj)
    dt.effectAllowed = 'move'
  }
  
  const onDragEnd = (e) => {
    setDragObj(null)
  }
  
  const onDragEnter = (e) => {
    const target = e.target.getAttribute('data-target')
    if (target != dragObj.gender) {
      return false
    }
    const dt = e.dataTransfer
    dt.dropEffect='move'
    e.preventDefault()
  }
  
  const onDragOver = (e) => {
    const target = e.target.getAttribute('data-target')
    if (target != dragObj.gender) {
      return false
    }

    const dt = e.dataTransfer
    dt.dropEffect='move'
    e.preventDefault()
  }
  
  const onDrop = (e) => {
    const dt = e.dataTransfer
    const obj = JSON.parse(dt.getData('text/json'))
    const effect = dt.dropEffect
    let mycouple = {...couple}
    if (obj.gender == 'f') {
      const remaining = _girls.filter(g => g.id != obj.id)
      // Return that girl to list
      if (couple.girl) {
        remaining.push(couple.girl)
      }
      setGirls(remaining)
      mycouple = {...mycouple, girl:obj}
    } else {
      const remaining = _guys.filter(g => g.id != obj.id)
      // Return that girl to list
      if (couple.guy) {
        remaining.push(couple.guy)
      }
      setGuys(remaining)
      mycouple = {...mycouple, guy:obj}
    }
    setDragObj(null)
    if (mycouple.girl && mycouple.guy) {
      setCouples([...couples, mycouple])
      setCouple({girl: null, guy: null})
    } else {
      setCouple(mycouple)
    }
    e.preventDefault()
  }
  
  const addCouple = () => {
    setCouples([...couples, couple])
    setCouple({girl: null, guy: null})
  }
  
  const removeCouple = (id) => {
    const couple = couples[id]
    setCouples(couples.filter(c => c != couple))
    setGuys([..._guys, couple.guy])
    setGirls([..._girls, couple.girl])
  }
  
  // Default - minWidth=768
  // Mobile - maxWidth=767
  return (
    <>
      <h1>Couples Editor</h1>
      <div className={classes.container}>
        <div className={classes.guys}>
          <ul>
            {_guys.map(guy => {
                return (
                  <li draggable
                      onDragStart={(e) => onDragStart(e, guy)}
                      onDragEnd={onDragEnd}
                  >{guy.name}</li>
                )
              }
            )}
          </ul>
        </div>
        <div className={classes.girls}>
          <ul>
            {_girls.map(g => {
                return (
                  <li draggable
                      onDragStart={(e) => onDragStart(e, g)}
                      onDragEnd={onDragEnd}
                  >{g.name}</li>
                )
              }
            )}
          </ul>
        </div>
        <div className={classes.couples}>
            {couples.map((couple, idx) => {
              return (
                <div className={classes.couple}>
                  <span>{`Couple: ${couple.girl.name} and ${couple.guy.name}`}</span>
                  <button onClick={() => removeCouple(idx)}>Remove</button>
                </div>
              )
            })}
        </div>
        <div className={classes.couple}>
          <div
            data-target="m"
            onDragOver={onDragOver}
            onDragEnter={onDragEnter}
            onDrop={onDrop}
            className={classes.guy}>
            {couple.guy ? couple.guy.name : ''}
          </div>
          <div
            data-target="f"
            onDragOver={onDragOver}
            onDragEnter={onDragEnter}
            onDrop={onDrop}
            className={classes.girl}>
            {couple.girl ? couple.girl.name : ''}
          </div>
        </div>
      </div>
    </>
  )
}

export default CouplesEditor
