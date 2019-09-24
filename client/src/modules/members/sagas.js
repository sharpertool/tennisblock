import {all, put, takeLatest, select, fork, call} from 'redux-saga/effects'
import axioscore from 'axios'

import * as actions from './actions'
import * as types from './constants'
import {moduleConfig} from './index'
import * as Sentry from '@sentry/browser'

const get_axios = () => {
  const {axios_config} = moduleConfig
  return axioscore.create(axios_config)
}

function* fetchBlockMembers() {
  const {apis: {blockmembers: url}} = moduleConfig
  const axios = get_axios()
  try {
    const {data} = yield call(axios.get, url)
    yield put(actions.updateBlockMembers(data))
  } catch (e) {
    Sentry.captureException(e)
  }
}

export default function* rootSaga() {
  yield all([
    fork(fetchBlockMembers),
  ])
}
