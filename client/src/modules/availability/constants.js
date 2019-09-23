export const NAME = 'availability'

const PARENT_NAME = 'parent'
export const APP_NAME = `${PARENT_NAME}/${NAME}`
const mkname = (nm) => `${APP_NAME}/${nm}`

export const UPDATE_BLOCK_DATES = mkname('UPDATE_BLOCK_DATES')

export const GET_AVAILABILITY = mkname('GET_AVAILABILITY')
export const UPDATE_AVAILABILITY = mkname('UPDATE_AVAILABILITY')

export const ON_PLAYER_AVAILABILITY_CHANGE = mkname('ON_PLAYER_AVAILABILITY_CHANGE')

export const UPDATE_PLAYER_AVAILABILITY = mkname('UPDATE_PLAYER_AVAILABILITY')

export const ON_ITEMS_SCROLL = mkname('ON_ITEMS_SCROLL')
