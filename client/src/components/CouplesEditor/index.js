import React, {useEffect, useState} from 'react'
import classes from './styles.local.scss'
import styled from 'styled-components'

import Couples from './Couples'
import CoupleTarget from './CoupleTarget'

const PlayerList = styled.ul`
  list-style: none;
  margin: 2px 2px;
  padding: 1px;
`
const ListItem = styled.li`
  padding: 2px;
  padding-left: 5px;
  border: 1px solid lightgrey;
  background-color: lightseagreen;
  border-radius: 2px;
`

const pluralize = nm => {
  return nm.charAt(nm.length - 1) == 's' ? nm + 'es' : nm + 's'
}

const build_name = couple => {
  const {girl, guy} = couple
  let name = ''
  if (girl.last == guy.last) {
    name = pluralize(girl.last)
  } else {
    name = `${girl.first} & ${guy.first}`
  }
  return name
}

const CouplesEditor = ({
                         guys,
                         girls,
                         couples,
                         addCouple,
                         removeCouple,
                         updateSingles,
                         updateFulltime,
                         updateName,
                       }) => {
  
  const default_couple = {
    name: '',
    guy: null,
    girl: null,
    as_singles: false,
    fulltime: false,
    blockcouple: true,
  }
  
  // Handle the drag-drop assignment locally with hooks
  const [couple, setCouple] = useState(default_couple)
  const [_guys, setGuys] = useState([])
  const [_girls, setGirls] = useState([])
  
  useEffect(() => {
    setGuys(guys)
    setGirls(girls)
  }, [guys, girls, couples])
  
  const onDragStart = (e, obj) => {
    const sobj = JSON.stringify(obj)
    const dt = e.dataTransfer
    dt.setData('text/json', sobj)
    dt.setData('text/plain', obj.id)
    dt.effectAllowed = 'move'
  }
  
  const onDragEnd = (e) => {
  }
  
  const onDragEnter = (e) => {
    const dt = e.dataTransfer
    dt.dropEffect = 'move'
    e.preventDefault()
  }
  
  const onDragOver = (e) => {
    const dt = e.dataTransfer
    dt.dropEffect = 'move'
    e.preventDefault()
  }
  
  const onDrop = (e) => {
    const dt = e.dataTransfer
    const obj = JSON.parse(dt.getData('text/json'))
    const effect = dt.dropEffect
    let mycouple = {...couple}
    if (obj.gender == 'F') {
      const remaining = _girls.filter(g => g.id != obj.id)
      // Return that girl to list
      if (couple.girl) {
        remaining.push(couple.girl)
      }
      setGirls(remaining)
      mycouple = {...mycouple, girl: obj}
    } else {
      const remaining = _guys.filter(g => g.id != obj.id)
      // Return that girl to list
      if (couple.guy) {
        remaining.push(couple.guy)
      }
      setGuys(remaining)
      mycouple = {...mycouple, guy: obj}
    }
    if (mycouple.girl && mycouple.guy) {
      const girl = mycouple.girl
      const guy = mycouple.guy
      mycouple.name = build_name(mycouple)
      mycouple.guy = guy.id
      mycouple.girl = girl.id
      addCouple(mycouple)
      setCouple(default_couple)
    } else {
      setCouple(mycouple)
    }
    e.preventDefault()
  }
  
  /**
   * removeCouple
   *
   * Return the girl and guy in the couple to the guy and girl lists
   * @param id
   */
  const onCoupleRemove = (idx) => {
    removeCouple({idx: idx})
  }
  
  const onSinglesChange = (e, idx) => {
    updateSingles({idx: idx, value: e.target.checked})
  }
  
  const onFulltimeChange = (e, idx) => {
    updateFulltime({idx: idx, value: e.target.checked})
  }
  
  const onCoupleNameChange = (e, idx) => {
    updateName({idx: idx, value: e.target.value})
  }
  
  return (
    <>
      <h1>Couples Editor</h1>
      <div className={classes.container}>
        <div className={classes.guys}>
          <PlayerList>
            {_guys.map((g, idx) => {
                return (
                  <ListItem
                    key={idx}
                    draggable
                    onDragStart={(e) => onDragStart(e, g)}
                    onDragEnd={onDragEnd}
                  >{`${g.first} ${g.last}`}</ListItem>
                )
              }
            )}
          </PlayerList>
        </div>
        <div className={classes.girls}>
          <PlayerList>
            {_girls.map((g, idx) => {
                return (
                  <ListItem
                    key={idx}
                    draggable
                    onDragStart={(e) => onDragStart(e, g)}
                    onDragEnd={onDragEnd}
                  >{`${g.first} ${g.last}`}</ListItem>
                )
              }
            )}
          </PlayerList>
        </div>
        <CoupleTarget
          grid_class={classes.couple}
          guy={couple.guy} girl={couple.girl}
          onDragEnter={onDragEnter}
          onDragOver={onDragOver}
          onDrop={onDrop}
        />
        <Couples
          div_class={classes.couples}
          couples={couples}
          onCoupleNameChange={onCoupleNameChange}
          onCoupleFulltimeChange={onFulltimeChange}
          onCoupleSinglesChange={onSinglesChange}
          onCoupleRemove={onCoupleRemove}
        />
      
      </div>
    </>
  )
}

export default CouplesEditor
