import {createConstants, createReducer} from 'redux-module-builder'
import { types as drawingTypes } from '../Drawing'

export const types = createConstants('modal')(
    'ZOOM_OPEN',
    'ZOOM_CLOSE',
    'ZOOM_TOGGLE',
    'DOWNLOAD_OPEN',
    'DOWNLOAD_CLOSE',
    'DOWNLOAD_TOGGLE'
)
export const initialState = {
    isOpen: false
}

export const actions = {}

export const reducer = createReducer({
    [drawingTypes.INITIALIZE](state, { dom_id }) {
        return {
            ...state,
            [`drawing-zoom-${dom_id}`]: {
                isOpen: false
            },
            [`drawing-download-${dom_id}`]: {
                isOpen: false
            }
        }
    },
    [types.ZOOM_TOGGLE](state, { dom_id }) {
        return {
            ...state,
            [`drawing-zoom-${dom_id}`]: {
                isOpen: !state[`drawing-zoom-${dom_id}`].isOpen
            }
        }
    },
    [types.ZOOM_OPEN](state, { dom_id }) {
        return {
            ...state,
            [`drawing-zoom-${dom_id}`]: {
                isOpen: true
            }
        }
    },
    [types.ZOOM_CLOSE](state, { dom_id }) {
        return {
            ...state,
            [`drawing-zoom-${dom_id}`]: {
                isOpen: false
            }
        }
    },
    [types.DOWNLOAD_OPEN](state, { dom_id }) {
        return {
            ...state,
            [`drawing-download-${dom_id}`]: {
                isOpen: true
            }
        }
    },
    [types.DOWNLOAD_CLOSE](state, { dom_id }) {
        return {
            ...state,
            [`drawing-download-${dom_id}`]: {
                isOpen: false
            }
        }
    },
    [types.DOWNLOAD_TOGGLE](state, { dom_id }) {
        return {
            ...state,
            [`drawing-download-${dom_id}`]: {
                isOpen: !state[`drawing-download-${dom_id}`].isOpen
            }
        }
    }
})
