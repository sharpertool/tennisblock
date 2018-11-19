// This file contains all the action creator functions

import * as types from './constants'

export const updatePlaySchedule = (schedule) => ({
  type: types.UPDATE_PLAY_SCHEDULE,
  payload: schedule
})


export const getBlockPlayers = (id) => {
  return {
    type: types.GET_BLOCK_PLAYERS,
    id
  }
}

export const setBlockPlayers = (blockplayers) => {
  console.log(types.BLOCK_PLAYERS_FETCHED)
  return { type: types.BLOCK_PLAYERS_FETCHED, blockplayers }
}