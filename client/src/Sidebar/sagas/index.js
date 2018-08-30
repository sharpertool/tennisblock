import {call, put, fork, takeEvery, takeLatest} from 'redux-saga/effects'
import ScrollSagas from './Scroll'

export default function* rootSaga() {
    yield fork(ScrollSagas)
}
