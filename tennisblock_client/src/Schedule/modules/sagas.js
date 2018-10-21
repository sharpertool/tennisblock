import {rootSaga as scheduleRoot} from './schedule'
import {rootSaga as teamRoot} from './teams'

import {fork} from 'redux-saga/effects'


export default function* rootSaga() {
  yield fork(scheduleRoot)
  yield fork(teamRoot)
}
