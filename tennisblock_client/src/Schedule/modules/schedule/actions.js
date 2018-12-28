import { createAction } from 'redux-actions'
import * as types from './constants'

export const setBlockDates = createAction(types.SET_BLOCKDATES)
export const updatePlaySchedule = createAction(types.UPDATE_PLAY_SCHEDULE)
export const getSubs = createAction(types.GET_SUBS)
export const changeBlockPlayer = createAction(types.BLOCK_PLAYER_CHANGED)
export const setBlockPlayers = createAction(types.FETCH_BLOCK_PLAYERS_SUCCEED)
export const getBlockPlayers = createAction(types.FETCH_BLOCK_PLAYERS)
export const getBlockPlayersFail = createAction(types.FETCH_BLOCK_PLAYERS_FAILED)
export const updateBlockPlayers = createAction(types.UPDATE_BLOCK_PLAYERS)
export const updateBlockPlayersFail = createAction(types.UPDATE_BLOCK_PLAYERS_FAILED)
export const clearSchedule = createAction(types.CLEAR_SCHEDULE)
export const clearScheduleFail = createAction(types.CLEAR_SCHEDULE_FAIL)
