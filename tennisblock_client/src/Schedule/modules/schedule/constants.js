import { actionType } from '~/utils'
export const MODULE_NAME = 'schedule'
export const PARENT_NAME = 'parent'
export const APP_NAME = `${PARENT_NAME}/${MODULE_NAME}`
const mkname = (nm) => `${APP_NAME}/${nm}`

export const SET_BLOCKDATES = mkname('SET_BLOCKDATES')

export const UPDATE_PLAY_SCHEDULE = mkname('UPDATE_PLAY_SCHEDULE')

export const FETCH_BLOCK_PLAYERS = mkname('FETCH_BLOCK_PLAYERS')
export const FETCH_BLOCK_PLAYERS_SUCCEED = mkname('FETCH_BLOCK_PLAYERS_SUCCEED')
export const FETCH_BLOCK_PLAYERS_FAILED = mkname('FETCH_BLOCK_PLAYERS_FAILED')
export const SET_BLOCK_PLAYERS = mkname('SET_BLOCK_PLAYERS')

export const UPDATE_BLOCK_PLAYERS = mkname('UPDATE_BLOCK_PLAYERS')
export const UPDATE_BLOCK_PLAYERS_FAILED = mkname('UPDATE_BLOCK_PLAYERS_FAILED')

export const GET_SUBS = mkname('GET_SUBS')
export const SET_SUBS = mkname('SET_SUBS')

export const BLOCK_PLAYER_CHANGED = mkname('BLOCK_PLAYER_CHANGED')

export const CLEAR_SCHEDULE = mkname('CLEAR_SCHEDULE')
export const CLEAR_SCHEDULE_FAIL = mkname('CLEAR_SCHEDULE_FAIL')
export const RE_SCHEDULE =mkname('RE_SCHEDULE')