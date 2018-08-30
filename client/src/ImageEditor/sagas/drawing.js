import { types } from '~/ImageEditor/modules/Drawing'
import {select, call, put, takeEvery, takeLatest} from 'redux-saga/effects'
import { imageToUrl } from './actions'

//Drawing states
export const selector = state => state.Drawing

export function* setLineColor(action) {
    try {
        const _idk = yield select(selector)
        //put(action)
    } catch(error) {

    }
}
//use this if there is async
export function* addNewLine({ type, path }) {
    try {
        const currState = yield select(selector)
        //yield put({ type, path })
    } catch(error) {

    }
}

export function* useCurrentSettings(action) {
    try {
        const _idk = yield select(selector)
        console.log(_idk)
    } catch(error) {

    }
}

export function* convertImage(action) {
    try {
        const { image, dom_id } = action
        const blob = yield call(imageToUrl, image)
        yield put({ type: types.IMAGE_CONVERTED, blob, dom_id })
    } catch(error) {

    }
 }

export default function* drawingSagas() {
    yield takeEvery(types.INITIALIZE, convertImage)
    yield takeEvery(types.COLOR_SELECTED, setLineColor)
    yield takeEvery(types.START, addNewLine)
}
