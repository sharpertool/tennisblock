export const NAME = 'season'

const PARENT_NAME = 'parent'
export const APP_NAME = `${PARENT_NAME}/${NAME}`
const mkname = (nm) => `${APP_NAME}/${nm}`

export const SAVE_COUPLES = mkname('SAVE_COUPLES')
export const UPDATING_COUPLES = mkname('UPDATING_COUPLES')
export const UPDATE_COUPLES = mkname('UPDATE_COUPLES')
export const UPDATE_PLAYERS = mkname('UPDATE_PLAYERS')

export const UPDATE_COUPLES_SUCCESS = mkname('UPDATE_COUPLES_SUCCESS')
export const UPDATE_COUPLES_FAIL = mkname('UPDATE_COUPLES_FAIL')

export const ADD_COUPLE = mkname('ADD_COUPLE')
export const REMOVE_COUPLE = mkname('REMOVE_COUPLE')
export const COUPLE_CHANGE_SINGLES = mkname('COUPLE_CHANGE_SINGLES')
export const COUPLE_CHANGE_FULLTIME = mkname('COUPLE_CHANGE_FULLTIME')
export const COUPLE_CHANGE_NAME = mkname('COUPLE_CHANGE_NAME')

