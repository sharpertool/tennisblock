import { createAction } from 'redux-actions'
import * as types from './constants'

export const setBlockDates = createAction(
    types.SET_BLOCKDATES,
    blockdates => ({ blockdates })
)

export const updatePlaySchedule = createAction(
    types.UPDATE_PLAY_SCHEDULE,
    schedule => ({ schedule })
)

export const getSubs = createAction(
    types.GET_SUBS,
    subs => ({ subs })
)

export const changeBlockPlayer = createAction(
    types.BLOCK_PLAYER_CHANGED,
    selectedPlayer => ({ selectedPlayer })
)

export const setBlockPlayers = createAction(
    types.FETCH_BLOCK_PLAYERS_SUCCEED,
    blockplayers => ({ blockplayers })
)

export const getBlockPlayers = createAction(
    types.FETCH_BLOCK_PLAYERS,
    blockDate => ({ blockDate })
)

export const getBlockPlayersFail = createAction(
    types.FETCH_BLOCK_PLAYERS_FAILED
)
