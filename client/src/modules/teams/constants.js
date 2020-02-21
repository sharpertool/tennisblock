export const NAME = 'teams'

const PARENT_NAME = 'parent'
export const APP_NAME = `${PARENT_NAME}/${NAME}`
const mkname = (nm) => `${APP_NAME}/${nm}`

export const UPDATE_MATCH_DATA = mkname('UPDATE_MATCH_DATA')
export const CALCULATE_MATCHUPS = mkname('CALCULATE_MATCHUPS')
export const UPDATE_CALCULATE_STATUS = mkname('UPDATE_CALCULATE_STATUS')
export const FETCH_CURRENT_SCHEDULE = mkname('FETCH_CURRENT_SCHEDULE')

export const RECALCULATE_MATCH = mkname('RECALCULATE_MATCH')
export const MATCH_CALCULATING = mkname('MATCH_CALCULATING')
export const CALCULATION_UPDATE = mkname('CALCULATION_UPDATE')

export const UPDATE_CALC_VALUE = mkname('UPDATE_CALC_VALUE')


