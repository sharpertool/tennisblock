export const NAME = 'schedule'

const PARENT_NAME = 'parent'
export const APP_NAME = `${PARENT_NAME}/${NAME}`
const mkname = (nm) => `${APP_NAME}/${nm}`

export const SET_BLOCKDATES = mkname('SET_BLOCKDATES')

export const UPDATE_PLAY_SCHEDULE = mkname('UPDATE_PLAY_SCHEDULE')

export const FETCH_BLOCK_PLAYERS = mkname('FETCH_BLOCK_PLAYERS')
export const FETCH_BLOCK_PLAYERS_SUCCEED = mkname('FETCH_BLOCK_PLAYERS_SUCCEED')
export const FETCH_BLOCK_PLAYERS_FAILED = mkname('FETCH_BLOCK_PLAYERS_FAILED')
export const SET_BLOCK_PLAYERS = mkname('SET_BLOCK_PLAYERS')

export const UPDATE_BLOCK_PLAYERS = mkname('UPDATE_BLOCK_PLAYERS')
export const UPDATE_BLOCK_PLAYERS_FAILED = mkname('UPDATE_BLOCK_PLAYERS_FAILED')

export const GET_SUBS = mkname('GET_SUBS')
export const SET_SUBS = mkname('SET_SUBS')

export const UPDATE_VERIFY_STATUS = mkname('UPDATE_VERIFY_STATUS')

export const BLOCK_PLAYER_CHANGED = mkname('BLOCK_PLAYER_CHANGED')

export const CLEAR_SCHEDULE = mkname('CLEAR_SCHEDULE')
export const CLEAR_SCHEDULE_FAIL = mkname('CLEAR_SCHEDULE_FAIL')

export const RE_SCHEDULE =mkname('RE_SCHEDULE')
export const RE_SCHEDULE_FAIL =mkname('RE_SCHEDULE_FAIL')

export const SCHEDULE_NOTIFY = mkname('SCHEDULE_NOTIFY')
export const SCHEDULE_NOTIFY_SUCCESS = mkname('SCHEDULE_NOTIFY_SUCCESS')
export const SCHEDULE_NOTIFY_FAIL = mkname('SCHEDULE_NOTIFY_FAIL')
export const SCHEDULE_NOTIFY_STARTED = mkname('SCHEDULE_NOTIFY_STARTED')
export const SCHEDULE_NOTIFY_MSG_UPDATE = mkname('SCHEDULE_NOTIFY_MSG_UPDATE')

export const NOTIFY_PLAYER = mkname('NOTIFY_PLAYER')
export const NOTIFY_PLAYER_SUCCESS = mkname('NOTIFY_PLAYER_SUCCESS')
export const NOTIFY_PLAYER_FAIL = mkname('NOTIFY_PLAYER_FAIL')

export const MANUAL_VERIFY_PLAYER = mkname('MANUAL_VERIFY_PLAYER')



