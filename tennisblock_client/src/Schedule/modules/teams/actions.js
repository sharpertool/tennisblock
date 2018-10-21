// This file contains all the action creator functions

import * as types from './constants'

export const updatePlaySchedule = (schedule) => ({
  type: types.UPDATE_PLAY_SCHEDULE,
  payload: schedule
})
