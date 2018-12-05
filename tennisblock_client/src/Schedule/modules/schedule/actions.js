import * as types from './constants'

export const setBlockDates = (blockdates) => ({
  type: types.SET_BLOCKDATES,
  payload: {
    blockdates
  }
})

export const updatePlaySchedule = (schedule) => ({
  type: types.UPDATE_PLAY_SCHEDULE,
  payload: schedule
})

export const getSubs = (subs) => ({
  type: types.GET_SUBS,
  payload: {
    subs
  }
})

export const changeBlockPlayer = (selectedPlayer) => ({
  type: types.BLOCK_PLAYER_CHANGED,
  payload: {
    selectedPlayer
  }
})

export const setBlockPlayers = (blockplayers) => ({
  type: types.FETCH_BLOCK_PLAYERS_SUCCEED,
  payload: {
    blockplayers
  }
})

export const getBlockPlayers = (blockDate) => ({
  type: types.FETCH_BLOCK_PLAYERS,
  payload: {
    blockDate
  }
})

export const getBlockPlayersFail = (error) => ({
  type: types.FETCH_BLOCK_PLAYERS_FAILED,
  payload: new Error(),
  error: true
})
