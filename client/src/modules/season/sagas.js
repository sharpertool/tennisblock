import {all, put, takeLatest, select, fork, call} from 'redux-saga/effects'
import {getCouples, getSubs} from './selectors'
import {get_global_selectors} from './index'
import axios_core from 'axios'
import axios from '~/axios-tennisblock'

import * as actions from './actions'
import * as types from './constants'


export default function* rootSaga() {
  yield all([
  ])
}
