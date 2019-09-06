import React, {createContext, useContext, useEffect, useState} from 'react'
import classes from './styles.local.scss'
import styled from 'styled-components'

import Couples from './Couples'
import CoupleTarget from './CoupleTarget'

export const dndContext = createContext()

const DragDrop = (props) => {
  
  const {children} = props
  
  const ctx = useContext(dndContext)
  
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
    // const target = e.target.getAttribute('data-target')
    // if (target != dragObj.gender) {
    //   return false
    // }
    const dt = e.dataTransfer
    dt.dropEffect = 'move'
    e.preventDefault()
  }
  
  const onDragOver = (e) => {
    // const target = e.target.getAttribute('data-target')
    // if (target != dragObj.gender) {
    //   return false
    // }
    //
    const dt = e.dataTransfer
    dt.dropEffect = 'move'
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
    setDragObj(null)
    if (mycouple.girl && mycouple.guy) {
      const girl = mycouple.girl
      const guy = mycouple.guy
      mycouple.name = build_name(mycouple)
      setCouples([...couples, mycouple])
      setCouple(default_couple)
    } else {
      setCouple(mycouple)
    }
    e.preventDefault()
  }
  
  return render(
    {children()}
  )
  
}

export default DragDrop
