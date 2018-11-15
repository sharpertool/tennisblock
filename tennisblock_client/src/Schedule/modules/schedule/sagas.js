import {all, put, take, race, fork, cancel, cancelled, call} from 'redux-saga/effects'

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

    const { data } = yield call(axios.get, '/api/blockdates')
    console.log(data)
    yield put({ type: types.SET_BLOCKDATES, blockdates: data })
  } catch ({ response }) {
    console.log(response)
  }

}

export default function* rootSaga() {
  yield all([
    fetchBlockDates(),
    requestInitialData(),
  ])
}
