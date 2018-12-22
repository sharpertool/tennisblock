// This file contains all the action creator functions

import * as types from './constants'

export const updatePlaySchedule = (schedule) => ({
  type: types.UPDATE_PLAY_SCHEDULE,
  payload: schedule
})

export const updateMatchData = (data) => ({
  type: types.UPDATE_MATCH_DATA,
  payload: data
})


export const getBlockPlayers = (id) => {
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

export const setBlockPlayers = (blockplayers) => {
  console.log(types.BLOCK_PLAYERS_FETCHED)
  return { type: types.BLOCK_PLAYERS_FETCHED, blockplayers }
}