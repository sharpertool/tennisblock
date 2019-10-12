import {put, call, all, takeLatest, select, fork} from 'redux-saga/effects'
import axioscore from 'axios'

const instance = axioscore.create({
  // ToDo: need a solution that works for deployed app.
  //baseURL: `${window.location.protocol}//${window.location.host}`,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken'
})

import {selectors, actions} from '~/redux-page'
import * as types from './constants'
import {moduleConfig} from './index'


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
    timeout: 10*60*1000,
  })
  
  const {date, iterations, tries, fpartner, fteam} = action.payload
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

export default function* rootSaga() {
  yield all([
    takeLatest(types.FETCH_CURRENT_SCHEDULE, fetchCurrentSchedule),
    takeLatest(types.CALCULATE_MATCHUPS, calculateMatchups),
  ])
}
