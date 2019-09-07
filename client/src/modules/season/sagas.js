import {all, put, takeLatest, takeEvery, select, fork, call} from 'redux-saga/effects'

import axioscore from 'axios'

import {actions, selectors} from '~/redux-page'
import {moduleConfig} from './index'
import * as types from './constants'
import * as Sentry from '@sentry/browser'

const get_axios = () => {
  const {axios_config} = moduleConfig
  return axioscore.create(axios_config)
}

function* fetchCouplesData() {
  const {couples_url} = moduleConfig
  
  const axios = get_axios()
  
  try {
    const {data} = yield call(axios.get, couples_url)
    const {players, couples} = data
    yield put(actions.updatePlayers(players))
    yield put(actions.updateCouples(couples))
  } catch (e) {
    Sentry.captureException(e)
  }
}

function* saveCouples(date) {
  const {couples_url} = moduleConfig
  const {getCouplesRaw} = selectors
  const couples = yield select(getCouplesRaw)
  
  const postdata = {couples: couples}
  
  const url = couples_url
  
  const axios = get_axios()
  try {
    yield put(actions.updatingCouples())
    const result = yield call(axios.post, url, postdata)
    const {data} = result
    const {status, created, updated} = data
    if (status == 'success') {
      yield put(actions.updateCouplesSuccess())
      yield fork(fetchCouplesData)
    } else {
      yield put(actions.updateCouplesFail())
    }
  } catch (e) {
    Sentry.captureException(e)
    yield put(actions.updateCouplesFail({error: e}))
  }
}

export default function* rootSaga() {
  yield all([
    fork(fetchCouplesData),
    
    yield takeEvery(types.COUPLE_SAVE_CHANGES, saveCouples),

  ])
}
