import {all, put, takeLatest, select, fork, call} from 'redux-saga/effects'
import {selectors, actions} from '~/redux-page'
import axioscore from 'axios'
import {moduleConfig} from './index'

import * as types from './constants'
import * as Sentry from '@sentry/browser'

const get_axios = () => {
  const {axios_config} = moduleConfig
  return axioscore.create(axios_config)
}

function* fetchBlockDates() {
  const {api: {blockdates: url}} = moduleConfig
  const axios = get_axios()
  try {
    const {data} = yield call(axios.get, url)
    yield put(actions.setBlockDates(data))
  } catch (e) {
    Sentry.captureException(e)
  }
}

function* requestMatchData(date) {
  const {api: {matchdata: urlpattern}} = moduleConfig
  
  const url = urlpattern.replace('0000-00-00', date)
  console.log(`Retrieve match data from ${url}`)
  
  const axios = get_axios()
  const response = yield call(axios.get, url)
  yield put(actions.updatePlaySchedule(response.data))
}


function* requestBlockPlayers({payload: date}) {
  const {api: {blockplayers: urlpattern}} = moduleConfig
  const {api: {subs: subspattern}} = moduleConfig
  const url = urlpattern.replace('0000-00-00', date)
  const suburl = subspattern.replace('0000-00-00', date)

  const axios = get_axios()
  try {
    yield fork(requestMatchData, date)

    const {data} = yield call(axios.get, url)
    yield put(actions.fetchBlockPlayersSuccess())
    yield put(actions.setBlockPlayers(data))
    {
      const {data} = yield call(axios.get, suburl)
      yield put(actions.setSubs(data))
    }
  } catch (error) {
    yield put(actions.getBlockPlayersFail(error))
    Sentry.captureException(error)
  }
}

function* updateBlockPlayersRequest({payload}) {
  const {getCouples, currentDate} = selectors
  const couples = yield select(getCouples)
  const date = yield select(currentDate)

  const {api: {blockplayers: urlpattern}} = moduleConfig
  const url = urlpattern.replace('0000-00-00', date)

  const axios = get_axios()
  try {
    const {data} = yield call(axios.post, url, {couples: couples})

    yield put(actions.getBlockPlayers(date))
  } catch (error) {
    yield put(actions.updateBlockPlayersFail(error))
    Sentry.captureException(error)
  }
}

function* clearScheduleRequest() {
  const {currentDate} = selectors
  const date = yield select(currentDate)

  const {api: {blockschedule: urlpattern}} = moduleConfig
  const url = urlpattern.replace('0000-00-00', date)

  const axios = get_axios()
  try {
    yield call(axios.delete, url)
    yield call(requestBlockPlayers, {payload: date})
  } catch (error) {
    yield put(actions.clearScheduleFail(error))
    Sentry.captureException(error)
  }
}

function* reScheduleRequest() {
  const {currentDate} = selectors
  const date = yield select(currentDate)

  const {api: {blockschedule: urlpattern}} = moduleConfig
  const url = urlpattern.replace('0000-00-00', date)

  const axios = get_axios()
  try {
    const { data } = yield call(axios.post, url)
    yield put(actions.setBlockPlayers(data))
  } catch (error) {
    yield put(actions.reScheduleFail(error))
    Sentry.captureException(error)
  }
}

function* scheduleNotify() {
  const {currentDate} = selectors
  const date = yield select(currentDate)

  const {api: {blockschedule: urlpattern}} = moduleConfig
  const url = urlpattern.replace('0000-00-00', date)

  // Send email notification to everyone scheduled for this meeting
  const {getCouples} = selectors
  const couples = yield select(getCouples)

  const axios = get_axios()

  try {
    const { data } = yield call(axios.post, url)
    yield put(actions.setBlockPlayers(data))
  } catch (error) {
    yield put(actions.reScheduleFail(error))
    Sentry.captureException(error)
  }
  
}

export default function* rootSaga() {
  yield all([
    fetchBlockDates(),
    takeLatest(types.FETCH_BLOCK_PLAYERS, requestBlockPlayers),
    takeLatest(types.UPDATE_BLOCK_PLAYERS, updateBlockPlayersRequest),
    takeLatest(types.CLEAR_SCHEDULE, clearScheduleRequest),
    takeLatest(types.RE_SCHEDULE, reScheduleRequest),
    takeLatest(types.SCHEDULE_NOTIFY, scheduleNotify)
  ])
}
