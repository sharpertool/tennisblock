import {createConstants, createReducer} from 'redux-module-builder'
import cond from 'lodash/cond'
import conforms from 'lodash/conforms'
import constant from 'lodash/constant'


export const types = createConstants('scroll')(
    'INITIALIZE',
    'GET_CONTENT',
    'CONTENT_LOADED',
    'APPEND_CONTENT',
    'PREPEND_CONTENT',
    'GET_PREV_CONTENT',
    'GET_DIRECT_CONTENT',
    'GET_NEXT_CONTENT',
    'SET_ACTIVE_CONTENT'
)

export const initialState = {
    contents: [],
    prepending: false,
    appending: false,
}

export const action = {}

export const reducer = createReducer({
    [types.INITIALIZE](state, { sidebar_data }) {
        return {
            ...state,
            sidebar_data
        }
    },
    [types.GET_NEXT_CONTENT](state) {
        return {
            ...state,
            appending: true
        }
    },
    [types.GET_PREV_CONTENT](state) {
        return {
            ...state,
            prepending: true
        }
    },
    [types.GET_DIRECT_CONTENT](state) {
        return {
            ...state,
            contents: [],
            isLoading: true
        }
    },
    [types.SET_ACTIVE_CONTENT](state, { active_content }) {
        return {
            ...state,
            active_content
        }
    },
    [types.CONTENT_LOADED](state, { contents }) {
        return {
            ...state,
            contents
        }
    },
    [types.APPEND_CONTENT](state, { contents }) {
        return {
            ...state,
            appending: false,
            contents: [...state.contents, contents]
        }
    },
    [types.PREPEND_CONTENT](state, { contents }) {
        return {
            ...state,
            prepending: false,
            contents: [contents, ...state.contents]
        }
    }
})
