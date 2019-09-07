import { createAction } from 'redux-actions'
import * as types from './constants'

export const saveCouples = createAction(types.SAVE_COUPLES)
export const updateCouples = createAction(types.UPDATE_COUPLES)
export const updatePlayers = createAction(types.UPDATE_PLAYERS)

export const updatingCouples = createAction(types.UPDATING_COUPLES)

export const updateCouplesSuccess = createAction(types.UPDATE_COUPLES_SUCCESS)
export const updateCouplesFail = createAction(types.UPDATE_COUPLES_FAIL)

export const addCouple = createAction(types.ADD_COUPLE)
export const removeCouple = createAction(types.REMOVE_COUPLE)
export const coupleChangeSingles = createAction(types.COUPLE_CHANGE_SINGLES)
export const coupleChangeFulltime = createAction(types.COUPLE_CHANGE_FULLTIME)
export const coupleChangeName = createAction(types.COUPLE_CHANGE_NAME)
export const coupleSaveChanges = createAction(types.COUPLE_SAVE_CHANGES)
