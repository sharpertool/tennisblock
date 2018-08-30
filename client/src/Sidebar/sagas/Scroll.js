import { select, call, put, takeEvery, takeLatest } from 'redux-saga/effects'
import { types } from '~/Sidebar/modules/Scroll'
import {
    fetchContents,
    fetchPrevContents,
    fetchNextContents,
    fetchDirectContents
} from './actions'

const data = state => {
    return state.Scroll.sidebar_data
}

export function* getContents({ sidebar_data }) {
    try {
        const contents = yield call(fetchContents, sidebar_data)
        yield put({ type: types.CONTENT_LOADED, contents })
    } catch(err) {
        console.log(err)
    }
}

export function* getPrevContents({ first_child }) {
    try {
        const sidebar_data = yield select(data)
        const contents = yield call(fetchPrevContents, sidebar_data, first_child)
        yield put({ type: types.PREPEND_CONTENT, contents })
    } catch(err) {
        console.log(err)
    }
}

export function* getNextContents({ last_child }) {
    try {
        const sidebar_data = yield select(data)
        const contents = yield call(fetchNextContents, sidebar_data, last_child)
        yield put({ type: types.APPEND_CONTENT, contents })
    } catch(err) {
        console.log(err)
    }
}

export function* getDirectContent({ slug }) {
    try {
        const sidebar_data = yield select(data)
        const contents = yield call(fetchDirectContents, sidebar_data, slug)
        yield put({ type: types.CONTENT_LOADED, contents })
    } catch(err) {
        console.log(err)
    }
}

export default function* ScrollSagas() {
    yield takeEvery(types.INITIALIZE, getContents)
    yield takeLatest(types.GET_PREV_CONTENT, getPrevContents)
    yield takeLatest(types.GET_NEXT_CONTENT, getNextContents)
    yield takeLatest(types.GET_DIRECT_CONTENT, getDirectContent)
}
