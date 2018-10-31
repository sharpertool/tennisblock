import {all, put, take, race, fork, cancel, cancelled, call} from 'redux-saga/effects'

import axios from '~/axios-tennisblock'

import * as actions from './actions'
import * as t from './constants'

function* requestUserProfile() {
  try {
    // const response = yield call(axios.get, 'api/profile/')
    // console.log(`Profile request returned:`, response.data)
    // const {status, profile} = response.data
    // if (status === 'success') {
    //   yield put(actions.updateProfile(profile))
    // }
  } catch (error) {
  
  }
}

function* requestInitialData() {
  yield fork(requestUserProfile)
}

export default function* rootSaga() {
  yield all([
    requestInitialData(),
  ])
}
