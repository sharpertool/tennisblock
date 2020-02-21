import {put, call, all, takeLatest, select, fork} from 'redux-saga/effects'
import axioscore from 'axios'

import {connectionManager} from '~/websockets_sagas'

const instance = axioscore.create({
  // ToDo: need a solution that works for deployed app.
  //baseURL: `${window.location.protocol}//${window.location.host}`,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken'
})

import {selectors, actions} from '~/redux-page'
import * as types from './constants'
import {moduleConfig} from './index'

function* channelsConnectionManager() {
  //const {comment_group, enable_wss} = moduleConfig

  // if (!enable_wss) {
  //   return yield delay(1)
  // }

  const url = '/ws/mixer/'

  console.log('Yielding to the master connection manager')
  yield connectionManager(url, actions, {
    onnconnect_send: {'action': 'getMixerStatus'}
  })
}

function* fetchCurrentSchedule({payload: {date}}) {
  const {apis: {matchdata}} = moduleConfig

  const url = matchdata.replace('0000-00-00', date)
  console.log(`Query match data at ${url}`)

  try {
    const {data} = yield call(instance.get, url)
    yield put(actions.updateMatchData(data.match))
  } catch ({response}) {
    console.log(response)
  }
}

function* calculateMatchups(action) {
  const {apis: {pickteams}} = moduleConfig

  const axios = axioscore.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    timeout: 10 * 60 * 1000,
  })

  const {date, iterations, tries, fpartner, fteam, low_threshold} = action.payload
  const url = pickteams.replace('0000-00-00', date)
  try {
    const {data} = yield call(axios.post,
      url,
      action.payload)
    if (data.status == 'success') {
      yield put(actions.updateMatchData(data.match))
    }
    yield put(actions.updateCalcResults({status: data.status, error: data.error}))
  } catch (e) {
    console.log(`Error picking teams. Will try again if you click! ${e}`)
  }
}

function* recalculateMatch(action) {

  const {apis: {recalculate_match}} = moduleConfig

  const {
    get_iterations, get_tries,
    get_fpartner, get_fteam, get_low_threshold
  } = selectors
  const iterations = yield select(get_iterations)
  const tries = yield select(get_tries)
  const fpartner = yield select(get_fpartner)
  const fteam = yield select(get_fteam)
  const low_threshold = yield select(get_low_threshold)

  const axios = axioscore.create({
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
    timeout: 10 * 60 * 1000,
  })

  const {date, setnumber} = action.payload

  const post_data = {
    date: date,
    setnumber: setnumber,
    iterations:iterations,
    tries: tries,
    fpartner: fpartner,
    fteam: fteam,
    low_threshold: low_threshold
  }

  let url = recalculate_match.replace('0000-00-00', date)
  url = url.replace('/0/', `/${setnumber}/`)

  console.log(`Call url: ${url}`)

  try {
    const {data} = yield call(axios.post,
      url,
      post_data)
    if (data.status == 'success') {
      yield put(actions.updateMatchData(data.match))
    }
    yield put(actions.updateCalcResults({status: data.status, error: data.error}))
  } catch (e) {
  console.log(`Error picking teams. Will try again if you click! ${e}`)
}
}

export default function* rootSaga() {
  yield all([
    fork(channelsConnectionManager),
    takeLatest(types.FETCH_CURRENT_SCHEDULE, fetchCurrentSchedule),
    takeLatest(types.CALCULATE_MATCHUPS, calculateMatchups),
    takeLatest(types.RECALCULATE_MATCH, recalculateMatch),
  ])
}
