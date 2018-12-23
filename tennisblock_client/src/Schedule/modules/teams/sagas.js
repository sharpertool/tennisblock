import { put, call, all, takeLatest, select, fork } from 'redux-saga/effects'
import axios from 'axios'

const instance = axios.create({
  // ToDo: need a solution that works for deployed app.
  baseURL: `${window.location.protocol}//${window.location.host}`,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken'
})

import * as actions from "./actions"
import * as types from './constants'


function* fetchCurrentSchedule() {
  try {
    console.log('Fetching latest play schedule')
    const { data } = yield call(instance.get, 'api/matchdata')
    console.log(`Latest play schedule: ${JSON.stringify(data)}`)
    yield put(actions.updateMatchData(data.match))
  } catch ({ response }) {
    console.log(response)
  }
}

function* calculateMatchups(action) {
  const date = action.payload
  console.log('Calculating new matchups')
  const {data} = yield call(instance.post, `api/pickteams/${date}`)
  console.log(data)
}

export default function* rootSaga() {
  yield all([
    fetchCurrentSchedule(),
    takeLatest(types.CALCULATE_MATCHUPS, calculateMatchups),
  ])
}
