import reducer from './reducers'

import {MODULE_NAME} from './constants'
import * as types from './constants'
import * as actions from './actions'
import * as selectors from './selectors'
import rootSaga from './sagas'

let global_selectors = {}
export const set_global_selectors = (gsel) => {
  global_selectors = gsel
}
export const get_global_selectors = () => {
  return global_selectors
}

import {APP_NAME} from './constants'
export {APP_NAME}
export {types, actions, selectors, MODULE_NAME, rootSaga};

export default reducer
