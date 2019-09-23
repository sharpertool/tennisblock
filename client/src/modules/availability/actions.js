import { createAction } from 'redux-actions'
import * as types from './constants'

export const getAvailability = createAction(types.GET_AVAILABILITY)
export const updateAvailability = createAction(types.UPDATE_AVAILABILITY)
export const updatePlayerAvailability = createAction(types.UPDATE_PLAYER_AVAILABILITY)
export const updateBlockDates = createAction(types.UPDATE_BLOCK_DATES)
export const onItemsScroll = createAction(types.ON_ITEMS_SCROLL)

export const onPlayerAvailabilityChange = createAction(types.ON_PLAYER_AVAILABILITY_CHANGE)
