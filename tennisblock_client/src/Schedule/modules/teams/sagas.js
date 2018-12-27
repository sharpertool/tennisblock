import {put, call, all, takeLatest, select, fork} from 'redux-saga/effects'
import axios from 'axios'

const instance = axios.create({
  // ToDo: need a solution that works for deployed app.
  //baseURL: `${window.location.protocol}//${window.location.host}`,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken'
})

import * as actions from "./actions"
import * as types from './constants'


function* fetchCurrentSchedule() {
  try {
    const {data} = yield call(instance.get, '/api/matchdata')
    yield put(actions.updateMatchData(data.match))
  } catch ({response}) {
    console.log(response)
  }
}

function* calculateMatchups(action) {
  const {date, iterations, tries} = action.payload
  try {
    const {data} = yield call(instance.post,
      `/api/pickteams/${date}`,
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
