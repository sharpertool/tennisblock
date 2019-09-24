export const NAME = 'members'

const PARENT_NAME = 'parent'
export const APP_NAME = `${PARENT_NAME}/${NAME}`
const mkname = (nm) => `${APP_NAME}/${nm}`

export const GET_BLOCK_MEMBERS = mkname('GET_BLOCK_MEMBERS')
export const GET_ALL_PLAYERS = mkname('GET_ALL_PLAYERS')

export const UPDATE_ALL_PLAYERS = mkname('UPDATE_ALL_PLAYERS')

export const UPDATE_BLOCK_MEMBERS = mkname('UPDATE_BLOCK_MEMBERS')
export const ON_BLOCK_MEMBER_CHANGED = mkname('ON_BLOCK_MEMBER_CHANGED')
