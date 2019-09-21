import {all, put, takeLatest, select, fork, call} from 'redux-saga/effects'
import {getCouples, getSubs} from './selectors'
import {get_global_selectors} from './index'
import axioscore from 'axios'

import * as actions from './actions'
import * as types from './constants'
import {moduleConfig} from './index'
import * as Sentry from '@sentry/browser'

const get_axios = () => {
  const {axios_config} = moduleConfig
  return axioscore.create(axios_config)
}

function* fetchAvailabilityData() {
  const {apis: {availability_url}} = moduleConfig
  
  const axios = get_axios()
  
  try {
    const {data} = yield call(axios.get, availability_url)
    console.log('Availability data:', data)
    yield put(actions.updateAvailability(data))
  } catch (e) {
    console.log(`Error fetching availability data ${e}`)
    Sentry.captureException(e)
  }
}

/*
 Payload should include:
 { id: xx, mtgidx: nn, isavail: true|false }
 */
function* updatePlayerAvailability({payload}) {
  const {apis: {availability_url}} = moduleConfig
  
  const axios = get_axios()
  
  try {
    const {data: {status}} = yield call(axios.put, availability_url, payload)
    // Response is {'status': 'success'} if passed.
    if (status == 'success') {
      yield put(actions.updatePlayerAvailability(payload))
    }
  } catch (e) {
    Sentry.captureException(e)
  }
  
}


export default function* rootSaga() {
  yield all([
    fork(fetchAvailabilityData),
  ])
}
