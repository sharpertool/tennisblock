import { createAction } from 'redux-actions'
import * as types from './constants'

export const getBlockMembers = createAction(types.GET_BLOCK_MEMBERS)

export const updateBlockMembers = createAction(types.UPDATE_BLOCK_MEMBERS)
