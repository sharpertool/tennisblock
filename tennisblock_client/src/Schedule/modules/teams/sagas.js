import {takeEvery, put, call} from 'redux-saga/effects'

import axios from '~/axios-tennisblock'

import * as actions from './actions'
import * as t from './constants'

function* requestMatchData(date) {
  const d = new Date(date)
  const matchDate = `${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()+1}`
  //console.log(`axios get for match data on ${date} using MatchDate:${matchDate}`)
  const response = yield call(axios.get, `/api/matchdata/${matchDate}`)
  //console.log('match response', response)
  yield put(actions.updatePlaySchedule(response.data))
  //console.log(response.data)
}

function* updateMatchData(action) {
  const date = action.payload
  //console.log(`Update Match data with date ${date}`)
  yield call(requestMatchData, date)
}

export default function* rootSaga() {
  yield takeEvery('UPDATE_CURRENT_DATE', updateMatchData)
}
