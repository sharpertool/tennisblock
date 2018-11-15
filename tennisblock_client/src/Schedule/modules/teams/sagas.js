import { all, put, take, race, fork, cancel, cancelled, call } from 'redux-saga/effects'

import axios from '~/axios-tennisblock'

import * as actions from './actions'

function* requestMatchData() {
  const date = '2018-09-21'
  const response = yield call(axios.get, '/api/matchdata')
  console.log(response)
  yield put(actions.updatePlaySchedule(response.data))
  console.log(response.data)
}

function* getBlockupdates() {

}


export default function* rootSaga() {
  yield all([
    requestMatchData()
  ])
}
