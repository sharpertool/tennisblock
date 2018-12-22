import { put, call, all } from 'redux-saga/effects'
import axios from '~/axios-tennisblock'
import * as actions from "./actions"

function* fetchCurrentSchedule() {
  try {
    console.log('Fetching latest play schedule')
    const { data } = yield call(axios.get, 'api/matchdata')
    console.log(`Latest play schedule: ${JSON.stringify(data)}`)
    yield put(actions.updateMatchData(data.match))
  } catch ({ response }) {
    console.log(response)
  }
}

export default function* rootSaga() {
  yield all([
    fetchCurrentSchedule()
  ])
}
