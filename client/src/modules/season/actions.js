import { createAction } from 'redux-actions'
import * as types from './constants'

export const saveCouples = createAction(types.SAVE_COUPLES)
export const updatingCouples = createAction(types.UPDATING_COUPLES)
export const updateCouples = createAction(types.UPDATE_COUPLES)
export const updatePlayers = createAction(types.UPDATE_PLAYERS)


export const updateCouplesSuccess = createAction(types.UPDATE_COUPLES_SUCCESS)
export const updateCouplesFail = createAction(types.UPDATE_COUPLES_FAIL)

