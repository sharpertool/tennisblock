import scheduleSagas from './schedule/sagas'
import teamSagas from './teams/sagas'

import { fork } from 'redux-saga/effects'


export default function* rootSaga() {
  yield fork(scheduleSagas)
  yield fork(teamSagas)
}
