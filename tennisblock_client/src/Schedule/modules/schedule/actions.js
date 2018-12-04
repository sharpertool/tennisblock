import * as types from './constants'

export const setBlockDates = ({ blockdates }) => ({ type: types.SET_BLOCKDATES, blockdates })

export const updatePlaySchedule = (schedule) => ({
  type: types.UPDATE_PLAY_SCHEDULE,
  payload: schedule
})


export const getBlockPlayers = (id) => {
  return {
    type: types.GET_BLOCK_PLAYERS,
    id,
  }
}

export const copyOriginalCouples = (couples) => {
    return {
        type: types.COPY_ORIGINAL_COUPLES,
        couples
    }
}

export const getSubs = (subs) => {
  return {
    type: types.GET_SUBS,
    subs,
  }
}

export const updateCouple = (selectedValue) => {
  return {
    type: types.UPDATE_COUPLE,
    selectedValue
  }
}

export const setBlockPlayers = (blockplayers) => {
  return { type: types.BLOCK_PLAYERS_FETCHED, blockplayers }
}
