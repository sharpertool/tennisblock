import clone from 'ramda/src/clone'
import {mergeDeepRightAll} from '~/modules/module_utils'
import * as R from 'ramda'
import { handleActions } from 'redux-actions'
import * as types from './constants'
import {
  groupByGenderAndId,
  toObjectById
} from './ramda_utils'

let configInitialState = {
}

export const update_initial_state = (initial_state) => {
  configInitialState = mergeDeepRightAll(configInitialState, initial_state)
}


const reducer = handleActions(
)

export default reducer
