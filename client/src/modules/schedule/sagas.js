import {all, put, takeLatest, select, fork, call} from 'redux-saga/effects'
import {selectors, actions} from '~/redux-page'
import axios_core from 'axios'
import axios from '~/axios-tennisblock'

import * as types from './constants'
import * as Sentry from '@sentry/browser'

function* requestUserProfile() {
  try {
    const response = yield call(axios.get, 'api/profile/')
    console.log('Profile request returned:', response.data)
    const {status, profile} = response.data
    if (status === 'success') {
      yield put(actions.updateProfile(profile))
    }
  } catch (e) {
    Sentry.captureException(e)
  }
}

function* requestInitialData() {
}

function* fetchBlockDates() {
  try {
    const {data} = yield call(axios.get, 'api/blockdates')
    yield put(actions.setBlockDates(data))
  } catch (e) {
    Sentry.captureException(e)
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
    yield put(actions.fetchBlockPlayersSuccess())
    yield put(actions.setBlockPlayers(data))
    {
      const {data} = yield call(axios.get, `/api/subs/${payload}`)
      yield put(actions.setSubs(data))
    }
  } catch (error) {
    yield put(actions.getBlockPlayersFail(error))
    Sentry.captureException(error)
  }
}

function* updateBlockPlayersRequest({payload}) {
  const {getCouples, currentData} = selectors
  const couples = yield select(getCouples)
  const date = yield select(currentDate)
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
    Sentry.captureException(error)
  }
}

function* clearScheduleRequest({payload}) {
  const {currentDate} = selectors
  const date = yield select(currentDate)
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
    Sentry.captureException(error)
  }
}

function* reScheduleRequest({ payload }) {
  const {currentDate} = selectors
  const date = yield select(currentDate)

  try {
    const instance = axios_core.create({
      baseURL: `${window.location.protocol}//${window.location.host}`,
      xsrfCookieName: 'csrftoken',
      xsrfHeaderName: 'X-CSRFToken'
    })
    const { data } = yield call(instance.post, `/api/blockschedule/${date}`)
    yield put(actions.setBlockPlayers(data))
  } catch (error) {
    yield put(actions.reScheduleFail(error))
    Sentry.captureException(error)
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

function* reSchedule() {
  yield takeLatest(types.RE_SCHEDULE, reScheduleRequest)
}


export default function* rootSaga() {
  yield all([
    fetchBlockDates(),
    requestInitialData(),
    getBlockPlayers(),
    updateBlockPlayers(),
    clearSchedule(),
    reSchedule()
  ])
}
