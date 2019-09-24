import { createAction } from 'redux-actions'
import * as types from './constants'

export const getBlockMembers = createAction(types.GET_BLOCK_MEMBERS)
export const getAllPlayers = createAction(types.GET_ALL_PLAYERS)

export const updateAllPlayers = createAction(types.UPDATE_ALL_PLAYERS)

export const updateBlockMembers = createAction(types.UPDATE_BLOCK_MEMBERS)
export const onBlockMemberChanged = createAction(types.ON_BLOCK_MEMBER_CHANGED)
export const toggleBlockSub = createAction(types.TOGGLE_BLOCK_SUB)
