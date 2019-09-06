export const NAME = 'season'

const PARENT_NAME = 'parent'
export const APP_NAME = `${PARENT_NAME}/${NAME}`
const mkname = (nm) => `${APP_NAME}/${nm}`

export const GET_AVAILABILITY = mkname('GET_AVAILABILITY')
