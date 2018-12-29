import {all, put, takeLatest, select, fork, call} from 'redux-saga/effects'
import {getCouples, getSubs} from './selectors'
import axios_core from 'axios'
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
  //yield fork(requestUserProfile)
}

function* fetchBlockDates() {
  try {
    const {data} = yield call(axios.get, 'api/blockdates')
    yield put(actions.setBlockDates(data))
  } catch ({response}) {
    console.log(response)
  }
}

function* requestMatchData(date) {
  const response = yield call(axios.get, `/api/matchdata/${date}`)
  yield put(actions.updatePlaySchedule(response.data))
}


function* requestBlockPlayers({payload}) {
  try {
    yield fork(requestMatchData, payload)

    const {data} = yield call(axios.get, `/api/blockplayers/${payload}`)
    yield put(actions.setBlockPlayers(data))
    
    const subs = yield call(axios.get, `/api/subs/${payload}`)
    yield put(actions.getSubs(subs.data))
  } catch (error) {
    yield put(actions.getBlockPlayersFail(error))
  }
}

function* updateBlockPlayersRequest({payload}) {
  const {date, couples} = payload
  try {
    const {data} = yield call((params) => {
      return axios.post(`/api/blockplayers/${date}`, params, {
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken'
      })
    }, {couples})
    
    yield put(actions.getBlockPlayers(date))
  } catch (error) {
    yield put(actions.updateBlockPlayersFail(error))
  }
}

function* clearScheduleRequest({payload}) {
  const {date} = payload
  try {
    const instance = axios_core.create({
      // ToDo: need a solution that works for deployed app.
      baseURL: `${window.location.protocol}//${window.location.host}`,
      xsrfCookieName: 'csrftoken',
      xsrfHeaderName: 'X-CSRFToken'
    })
    
    yield call(instance.delete, `/api/blockschedule/${date}`)
    yield call(requestBlockPlayers, {payload: date})
  } catch (error) {
    yield put(actions.clearScheduleFail(error))
  }
}

function* getBlockPlayers() {
  yield takeLatest(types.FETCH_BLOCK_PLAYERS, requestBlockPlayers)
}

function* updateBlockPlayers() {
  yield takeLatest(types.UPDATE_BLOCK_PLAYERS, updateBlockPlayersRequest)
}

function* clearSchedule() {
  yield takeLatest(types.CLEAR_SCHEDULE, clearScheduleRequest)
}


export default function* rootSaga() {
  yield all([
    fetchBlockDates(),
    requestInitialData(),
    getBlockPlayers(),
    updateBlockPlayers(),
    clearSchedule()
  ])
}
