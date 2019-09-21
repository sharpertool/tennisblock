import { createAction } from 'redux-actions'
import * as types from './constants'

export const getAvailability = createAction(types.GET_AVAILABILITY)
export const updateAvailability = createAction(types.UPDATE_AVAILABILITY)
export const updatePlayerAvailability = createAction(types.UPDATE_PLAYER_AVAILABILITY)
