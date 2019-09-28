// This file contains all the action creator functions
import { createAction } from 'redux-actions'

import * as types from './constants'

export const updateMatchData = createAction(types.UPDATE_MATCH_DATA)
export const calculateMatchups = createAction(types.CALCULATE_MATCHUPS)
export const updateCalcResults = createAction(types.UPDATE_CALCULATE_STATUS)
export const fetchCurrentSchedule = createAction(types.FETCH_CURRENT_SCHEDULE)
