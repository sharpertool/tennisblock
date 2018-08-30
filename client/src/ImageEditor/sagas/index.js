import {call, put, fork, takeEvery, takeLatest} from 'redux-saga/effects'
import drawingSagas from './drawing'

export default function* rootSaga() {
    yield fork(drawingSagas)
}
