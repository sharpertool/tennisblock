export const NAME = 'teams'
import {APP_NAME as PARENT_NAME} from '../constants'

const mkname = (nm) => `${PARENT_NAME}/${NAME}/${nm}`

export const APP_NAME = `${PARENT_NAME}/${NAME}`

export const UPDATE_PLAY_SCHEDULE = mkname('UPDATE_PLAY_SCHEDULE')









