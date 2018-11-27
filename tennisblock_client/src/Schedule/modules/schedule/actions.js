import * as types from './constants'

export const setBlockDates = ({ blockdates }) => ({ type: types.SET_BLOCKDATES, blockdates })

export const updatePlaySchedule = (schedule) => ({
  type: types.UPDATE_PLAY_SCHEDULE,
  payload: schedule
})


export const getBlockPlayers = (id) => {
  console.log(id)
  return {
    type: types.GET_BLOCK_PLAYERS,
    id,
  }
}

export const getSubs = (subs) => {
  return {
    type: types.GET_SUBS,
    subs,
  }
}

export const updateCouple = (prevPlayer, sub) => {
  return {
    type: types.UPDATE_COUPLE,
    prevPlayer,
    sub
  }
}

export const setBlockPlayers = (blockplayers) => {
  return { type: types.BLOCK_PLAYERS_FETCHED, blockplayers }
}