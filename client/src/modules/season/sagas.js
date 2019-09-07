import {all, put, takeLatest, takeEvery, select, fork, call} from 'redux-saga/effects'

import axioscore from 'axios'

import {actions, selectors} from '~/redux-page'
import {moduleConfig} from './index'
import * as types from './constants'

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
    console.log(`error happened ${e}`)
  }
}

function* saveCouples(date) {
  const {couples_url} = moduleConfig
  
  const data = {}
  const season_id = 23
  const url = couples_url
    .replace(/000/, season_id)
  
  const axios = get_axios()
  try {
    yield put(actions.updatingCouples())
    const result = yield call(axios.post, url, data)
    // ToDo: Check result status to insure it passed.
    yield put(actions.updateCouplesSuccess())
  } catch (e) {
    captureException(e)
    yield put(actions.updateCouplesFail({error: e}))
  }
}



export default function* rootSaga() {
  yield all([
    fork(fetchCouplesData),
    
    yield takeEvery(types.SAVE_COUPLES, saveCouples),

  ])
}
