import {all, put, take, race, fork, cancel, cancelled, call} from 'redux-saga/effects'

import axios from '~/axios-tennisblock'

import * as actions from './actions'
import * as t from './constants'

function* requestMatchData() {
  const date = '2018-10-26'
  const response = yield call(axios.get, `/api/matchdata/${date}`)
  yield put(actions.updatePlaySchedule(response.data))
  console.log(response.data)
}


export default function* rootSaga() {
  yield all([
    requestMatchData()
  ])
}
