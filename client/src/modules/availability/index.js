import {mergeDeepRightAll} from '~/modules/module_utils'
import reducer, {update_initial_state} from './reducers'
import {globalizeActions} from '../module_utils'

import {NAME} from './constants'
const optkey = `${NAME}_opts`
import * as types from './constants'
import * as actions from './actions'
export const gactions = globalizeActions(actions, NAME)
import * as selectors from './selectors'
import eventsMap from './eventsMap'
import rootSaga from './sagas'
import {APP_NAME} from './constants'
export {APP_NAME}
export {types, actions, selectors, eventsMap, NAME, rootSaga};

export let moduleConfig = {
  axios_config: {
    baseURL: '/',
  }
}


export const setConfig = ({defaults, options}) => {
  if (options && options[optkey]) {
    const myopts = options[optkey]
    if ('initial_state' in myopts) {
      update_initial_state(myopts.initial_state)
      delete myopts.initial_state
    }
    moduleConfig = mergeDeepRightAll(moduleConfig, defaults, myopts)
  } else {
    moduleConfig = mergeDeepRightAll(moduleConfig, defaults)
  }
}

export const initialize = () => {}

export default reducer
