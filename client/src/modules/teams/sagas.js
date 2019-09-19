import {put, call, all, takeLatest, select, fork} from 'redux-saga/effects'
import axios from 'axios'

const instance = axios.create({
  // ToDo: need a solution that works for deployed app.
  //baseURL: `${window.location.protocol}//${window.location.host}`,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken'
})

import * as actions from './actions'
import * as types from './constants'
import {moduleConfig} from './index'


function* fetchCurrentSchedule() {
  const {api: {matchdata}} = moduleConfig
  try {
    const {data} = yield call(instance.get, matchdata)
    yield put(actions.updateMatchData(data.match))
  } catch ({response}) {
    console.log(response)
  }
}

function* calculateMatchups(action) {
  const {api: {pickteams}} = moduleConfig
  
  const {date, iterations, tries, fpartner, fteam} = action.payload
  const url = pickteams.replace('0000-00-00', date)
  try {
    const {data} = yield call(instance.post,
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

export default function* rootSaga() {
  yield all([
    fetchCurrentSchedule(),
    takeLatest(types.CALCULATE_MATCHUPS, calculateMatchups),
  ])
}
