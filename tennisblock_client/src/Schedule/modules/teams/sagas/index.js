import { takeLatest, all, put, take, race, fork, cancel, cancelled, call } from 'redux-saga/effects'
import axios from '~/axios-tennisblock'

import * as actions from '~/Schedule/modules/teams/actions'
import * as types from '~/Schedule/modules/teams/constants' 

function* requestBlockPlayers(action) {
  try {
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


export default function* rootSaga() {
  yield all([
    setPlayers()
  ])
}
