import { actionType } from '~/utils'

export const MODULE_NAME = 'teams'

export const UPDATE_PLAY_SCHEDULE = actionType('UPDATE_PLAY_SCHEDULE', MODULE_NAME)

export const GET_BLOCK_PLAYERS = actionType('GET_BLOCK_PLAYERS', MODULE_NAME)

export const BLOCK_PLAYERS_FETCHED = actionType('BLOCK_PLAYERS_FETCHED', MODULE_NAME)

export const GET_SUBS = actionType('GET_SUBS', MODULE_NAME)