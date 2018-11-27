import {all, put, takeLatest, select, fork, call} from 'redux-saga/effects'
import { getCouples, getSubs } from './selectors'
import axios from '~/axios-tennisblock'

import * as actions from './actions'
import * as types from './constants'

function* requestUserProfile() {
  try {
     const response = yield call(axios.get, 'api/profile/')
     console.log(`Profile request returned:`, response.data)
     const {status, profile} = response.data
     if (status === 'success') {
       yield put(actions.updateProfile(profile))
     }
  } catch (error) {
  
  }
}

function* requestInitialData() {
  yield fork(requestUserProfile)
}

function* fetchBlockDates() {
  try {

    const { data } = yield call(axios.get, 'api/blockdates')
    yield put({
      type: types.SET_BLOCKDATES,
      blockdates: data.filter(date => !date.holdout)
    })
  } catch ({ response }) {
    console.log(response)
  }

}

function* requestMatchData() {
  const date = '2018-09-21'
  const response = yield call(axios.get, '/api/matchdata')
  console.log(response)
  yield put(actions.updatePlaySchedule(response.data))
  console.log(response.data)
}


function* requestBlockPlayers(action) {
  try {
    console.log(action)
    const { data } = yield call(axios.get, `/api/blockplayers/${action.id}`)
    yield put(actions.setBlockPlayers(data)) 
    const subs = yield call(axios.get, `/api/subs/${action.id}`)
    yield put(actions.getSubs(subs.data))
  } catch (error) {
    console.log(error.response)
  }
}

function* setPlayers() {
  yield takeLatest(types.GET_BLOCK_PLAYERS, requestBlockPlayers)
}



function* updateCouplePlayers(action) {
  const couples = yield select(getCouples)
  const subs = yield select(getSubs)
  console.log(couples, subs)
}

function* updateMatches() {
  yield takeLatest(types.UPDATE_COUPLE, updateCouplePlayers)
}


export default function* rootSaga() {
  yield all([
    fetchBlockDates(),
    requestInitialData(),
    setPlayers(),
    updateMatches()
  ])
}
