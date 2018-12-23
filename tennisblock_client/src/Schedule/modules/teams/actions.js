// This file contains all the action creator functions
import { createAction } from 'redux-actions'

import * as types from './constants'

export const updateMatchData = createAction(types.UPDATE_MATCH_DATA)
export const calculateMatchups = createAction(types.CALCULATE_MATCHUPS)
