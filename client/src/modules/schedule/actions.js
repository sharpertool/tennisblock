import { createAction } from 'redux-actions'
import * as types from './constants'

export const setCurrentDate = createAction(types.SET_CURRENT_DATE)

export const setBlockDates = createAction(types.SET_BLOCKDATES)
export const updatePlaySchedule = createAction(types.UPDATE_PLAY_SCHEDULE)
export const getSubs = createAction(types.GET_SUBS)
export const setSubs = createAction(types.SET_SUBS)
export const changeBlockPlayer = createAction(types.BLOCK_PLAYER_CHANGED)
export const onPlayerChanged = createAction(types.BLOCK_PLAYER_CHANGED)
export const onBlockPlayerChanged = createAction(types.BLOCK_PLAYER_CHANGED)
export const fetchBlockPlayersSuccess = createAction(types.FETCH_BLOCK_PLAYERS_SUCCEED)
export const setBlockPlayers = createAction(types.SET_BLOCK_PLAYERS)
export const getBlockPlayers = createAction(types.FETCH_BLOCK_PLAYERS)
export const getBlockPlayersFail = createAction(types.FETCH_BLOCK_PLAYERS_FAILED)
export const updateBlockPlayers = createAction(types.UPDATE_BLOCK_PLAYERS)
export const updateBlockPlayersFail = createAction(types.UPDATE_BLOCK_PLAYERS_FAILED)
export const clearSchedule = createAction(types.CLEAR_SCHEDULE)
export const clearScheduleFail = createAction(types.CLEAR_SCHEDULE_FAIL)
export const reSchedule = createAction(types.RE_SCHEDULE)
export const reScheduleFail = createAction(types.RE_SCHEDULE_FAIL)

// Notify
export const scheduleNotify = createAction(types.SCHEDULE_NOTIFY)
export const scheduleNotifySuccess = createAction(types.SCHEDULE_NOTIFY_SUCCESS)
export const scheduleNotifyFail = createAction(types.SCHEDULE_NOTIFY_FAIL)
export const scheduleNotifyStarted = createAction(types.SCHEDULE_NOTIFY_STARTED)
export const scheduleNotifyMsgUpdate = createAction(types.SCHEDULE_NOTIFY_MSG_UPDATE)
export const scheduleVerifyChanged = createAction(types.SCHEDULE_VERIFY_CHANGED)

export const updateVerifyStatus  = createAction(types.UPDATE_VERIFY_STATUS)

export const manualVerifyPlayer = createAction(types.MANUAL_VERIFY_PLAYER)

export const notifyPlayer = createAction(types.NOTIFY_PLAYER)
export const notifyPlayerSuccess = createAction(types.NOTIFY_PLAYER_SUCCESS)
export const notifyPlayerFail = createAction(types.NOTIFY_PLAYER_FAIL)

