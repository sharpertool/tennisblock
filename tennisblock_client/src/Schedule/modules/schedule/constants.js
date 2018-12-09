import { actionType } from '~/utils'
export const MODULE_NAME = 'schedule'

export const SET_BLOCKDATES = actionType('SET_BLOCKDATES', MODULE_NAME)

export const UPDATE_PLAY_SCHEDULE = actionType('UPDATE_PLAY_SCHEDULE', MODULE_NAME)

export const FETCH_BLOCK_PLAYERS = actionType('FETCH_BLOCK_PLAYERS', MODULE_NAME)
export const FETCH_BLOCK_PLAYERS_SUCCEED = actionType('FETCH_BLOCK_PLAYERS_SUCCEED', MODULE_NAME)
export const FETCH_BLOCK_PLAYERS_FAILED = actionType('FETCH_BLOCK_PLAYERS_FAILED', MODULE_NAME)

export const GET_SUBS = actionType('GET_SUBS', MODULE_NAME)

export const BLOCK_PLAYER_CHANGED = actionType('BLOCK_PLAYER_CHANGED', MODULE_NAME)
