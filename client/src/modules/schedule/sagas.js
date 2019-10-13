import {all, put, takeLatest, select, fork, call, delay} from 'redux-saga/effects'
import {selectors, actions} from '~/redux-page'
import axioscore from 'axios'
import {moduleConfig} from './index'

import {connectionManager} from '~/websockets_sagas'

import * as types from './constants'
import * as Sentry from '@sentry/browser'

const get_axios = () => {
  const {axios_config} = moduleConfig
  return axioscore.create(axios_config)
}

function* channelsConnectionManager() {
  const {currentDate} = selectors
  const date = yield select(currentDate)
  //const {comment_group, enable_wss} = moduleConfig
  
  // if (!enable_wss) {
  //   return yield delay(1)
  // }
  
  const url = `/ws/schedule/${date}/`
  
  console.log('Sockets URL:', url)
  
  console.log('Yielding to the master connection manager')
  yield connectionManager(url, actions, {
    onnconnect_send: {'action': 'getScheduleStatus'}
  })
}

function* fetchBlockDates() {
  const {apis: {blockdates: url}} = moduleConfig
  const axios = get_axios()
  try {
    const {data} = yield call(axios.get, url)
    yield put(actions.setBlockDates(data))
  } catch (e) {
    Sentry.captureException(e)
  }
}

function* requestMatchData(date) {
  const {apis: {matchdata: urlpattern}} = moduleConfig
  
  const url = urlpattern.replace('0000-00-00', date)
  //console.log(`Retrieve match data from ${url}`)
  
  const axios = get_axios()
  const response = yield call(axios.get, url)
  yield put(actions.updatePlaySchedule(response.data))
}

function* queryVerifyStatus(date) {
  const {apis: {verifystatus: verifypat}} = moduleConfig
  const url = verifypat.replace('0000-00-00', date)
  
  console.log(`query Verify status at ${url}`)
  const axios = get_axios()
  try {
    const {data} = yield call(axios.get, url)
    console.log('Verify status: ', data)
    const {status, results} = data
    yield put(actions.updateVerifyStatus(results))
  } catch (error) {
    Sentry.captureException(error)
  }
}

function* requestBlockPlayers({payload: {date}}) {
  //console.log(`Requets Block players for date ${date}`)
  const {apis: {blockplayers: urlpattern}} = moduleConfig
  const {apis: {subs: subspattern}} = moduleConfig
  
  
  const url = urlpattern.replace('0000-00-00', date)
  const suburl = subspattern.replace('0000-00-00', date)
  
  const axios = get_axios()
  try {
    yield fork(requestMatchData, date)
    yield fork(queryVerifyStatus, date)
    
    const {data} = yield call(axios.get, url)
    yield put(actions.fetchBlockPlayersSuccess())
    yield put(actions.setBlockPlayers(data))
    {
      const {data} = yield call(axios.get, suburl)
      yield put(actions.setSubs(data))
    }
    yield fork(channelsConnectionManager)
  } catch (error) {
    yield put(actions.getBlockPlayersFail(error))
    Sentry.captureException(error)
  }
}

function* updateBlockPlayersRequest({payload}) {
  const {getCouples, currentDate} = selectors
  const couples = yield select(getCouples)
  const date = yield select(currentDate)
  
  const {apis: {blockplayers: urlpattern}} = moduleConfig
  const url = urlpattern.replace('0000-00-00', date)
  
  const axios = get_axios()
  try {
    const {data} = yield call(axios.post, url, {couples: couples})
    
    yield put(actions.getBlockPlayers({date: date}))
  } catch (error) {
    yield put(actions.updateBlockPlayersFail(error))
    Sentry.captureException(error)
  }
}

function* clearScheduleRequest() {
  const {currentDate} = selectors
  const date = yield select(currentDate)
  
  const {apis: {blockschedule: urlpattern}} = moduleConfig
  const url = urlpattern.replace('0000-00-00', date)
  
  const axios = get_axios()
  try {
    yield call(axios.delete, url)
    yield call(requestBlockPlayers, {payload: {date:date}})
  } catch (error) {
    yield put(actions.clearScheduleFail(error))
    Sentry.captureException(error)
  }
}

function* reScheduleRequest() {
  const {currentDate} = selectors
  const date = yield select(currentDate)
  
  const {apis: {blockschedule: urlpattern}} = moduleConfig
  const url = urlpattern.replace('0000-00-00', date)
  
  const axios = get_axios()
  try {
    const {data} = yield call(axios.post, url)
    yield put(actions.setBlockPlayers(data))
    yield call(queryVerifyStatus, date)
  } catch (error) {
    yield put(actions.reScheduleFail(error))
    Sentry.captureException(error)
  }
}

function* scheduleNotify({payload: {message}}) {
  console.log('Message:', message)
  const {currentDate} = selectors
  const date = yield select(currentDate)
  
  const {apis: {notify: urlpattern}} = moduleConfig
  const url = urlpattern.replace('0000-00-00', date)
  
  const axios = get_axios()
  
  try {
    yield put(actions.scheduleNotifyStarted())
    const {data} = yield call(axios.post, url, {message: message})
    if (data.status == 'success') {
      yield put(actions.scheduleNotifySuccess())
    } else {
      yield put(actions.scheduleNotifyFail([data.message]))
    }
  } catch (error) {
    yield put(actions.scheduleNotifyFail([error]))
    Sentry.captureException(error)
  }
  
}

function* notifyPlayer({payload: {id}}) {
  const {currentDate} = selectors
  const date = yield select(currentDate)
  const {apis: {notify_player: apiurl}} = moduleConfig
  const url = apiurl
    .replace('000', id)
    .replace('0000-00-00', date)
  const axios = get_axios()
  try {
    const {data} = yield call(axios.post, url)
    if (data.status == 'success') {
    } else {
    }
    yield call(queryVerifyStatus, date)
  } catch (error) {
    Sentry.captureException(error)
  }
}

function* verifyPlayer({payload: {id}}) {
  const {currentDate} = selectors
  const {apis: {verify_player: apiurl}} = moduleConfig
  const date = yield select(currentDate)
  const url = apiurl
    .replace('000', id)
    .replace('0000-00-00', date)
  const axios = get_axios()
  
  console.log(`Verify player with ${url}`)
  try {
    const {data} = yield call(axios.post, url)
    if (data.status == 'success') {
    } else {
    }
    yield call(queryVerifyStatus, date)
  } catch (error) {
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
    takeLatest(types.SCHEDULE_NOTIFY, scheduleNotify),
    takeLatest(types.NOTIFY_PLAYER, notifyPlayer),
    takeLatest(types.MANUAL_VERIFY_PLAYER, verifyPlayer),
  ])
}
