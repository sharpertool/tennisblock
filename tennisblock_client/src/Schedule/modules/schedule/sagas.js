import {all, put, takeLatest, select, fork, call} from 'redux-saga/effects'
import { getCouples, getSubs } from './selectors'
import axios from '~/axios-tennisblock'

import * as actions from './actions'
import * as types from './constants'

function* requestUserProfile() {
  try {
     const response = yield call(axios.get, 'api/profile/')
     console.log(`Profile request returned:`, response.data)
     const {status, profile} = response.data
     if (status === 'success') {
       yield put(actions.updateProfile(profile))
     }
  } catch (error) {

  }
}

function* requestInitialData() {
  yield fork(requestUserProfile)
}

function* fetchBlockDates() {
  try {

    const { data } = yield call(axios.get, 'api/blockdates')
    yield put(actions.setBlockDates(data))
  } catch ({ response }) {
    console.log(response)
  }

}

function* requestMatchData(date) {
  const response = yield call(axios.get, `/api/matchdata/${date}`)
  console.log(response)
  yield put(actions.updatePlaySchedule(response.data))
  console.log(response.data)
}


function* requestBlockPlayers({ payload }) {
  try {
    yield fork(requestMatchData, payload.blockDate)
    
    const { data } = yield call(axios.get, `/api/blockplayers/${payload.blockDate}`)
    yield put(actions.setBlockPlayers(data))

    const subs = yield call(axios.get, `/api/subs/${payload.blockDate}`)
    yield put(actions.getSubs(subs.data))
  } catch (error) {
    yield put(actions.getBlockPlayersFail(error))
  }
}

function* getBlockPlayers() {
  yield takeLatest(types.FETCH_BLOCK_PLAYERS, requestBlockPlayers)
}


export default function* rootSaga() {
  yield all([
    fetchBlockDates(),
    requestInitialData(),
    getBlockPlayers()
  ])
}
