import {createConstants, createReducer} from 'redux-module-builder'

export const types = createConstants('drawing')(
    'ERROR',
    'START',
    'INITIALIZE',
    'IS_DRAWING',
    'COLOR_SELECTED',
    'UPDATE_SETTINGS',
    'ADD_NEW_LINE',
    'SET_ACTIVE_LINE',
    'SET_LINE_LAYER',
    'END',
    'ERASE_ALL',
    'TYPE_SELECTED',
    'IMAGE_CONVERTED'
)

export const initialState = {
    initialized: false,
    active_color: '#222222',
    paths: [],
    active_path: {
        path: [],
        color: ''
    },
    brush_tool_open: false,
    drawing_type: 'brush',
    isDrawing: false,
    palette_colors: [
        '#333333',
        '#ffffff',
        '#1b9e77',
        '#d95f02',
        '#7570b3',
        '#e7298a',
        '#66a61e',
        '#e6ab02',
        '#a6761d',
        '#666666'
    ],
}

export const actions = {}

export const reducer = createReducer({
    [types.INITIALIZE](state, { dom_id, image }){
        return {
            ...state,
            [`drawing-${dom_id}`]: {
                isDrawing: false,
                paths: [],
                image,
                active_color: '#222222',
                active_path: {
                    path: [],
                    color: ''
                },
                initialized: true,
                brush_tool_open: false,
                enabled: false
            },
            initialized: true
        }
    },
    [types.START](state, { path, stroke, dom_id }) {
        const curr_dom = state[`drawing-${dom_id}`]
        curr_dom.active_path.path.push(path)
        curr_dom.paths.push({
            stroke,
            path: curr_dom.active_path.path
        })
        return {
            ...state,
            [`drawing-${dom_id}`]: {
                ...curr_dom
            }
        }
    },
    [types.IS_DRAWING](state, { dom_id }) {
        const curr_dom = state[`drawing-${dom_id}`]

        return {
            ...state,
            [`drawing-${dom_id}`]: {
                ...curr_dom,
                isDrawing: true,
            }
        }
    },
    [types.ERASE_ALL](state, { dom_id }) {
        const curr_dom = state[`drawing-${dom_id}`]
        return {
            ...state,
            [`drawing-${dom_id}`]: {
                ...curr_dom,
                paths: [],
                active_color: '#222222',
                active_path: {
                    path: [],
                    color: ''
                },
                enabled: false,
                brush_tool_open: false
            }
        }
    },
    [types.END](state, { dom_id }) {
        const curr_dom = state[`drawing-${dom_id}`]
        return {
            ...state,
            [`drawing-${dom_id}`]: {
                ...curr_dom,
                isDrawing: false,
                active_path: {
                    path: [],
                    color: ''
                },
                path: [ ]
            }
        }
    },
    [types.COLOR_SELECTED](state, { active_color, brush_tool_open, dom_id }) {
        const curr_dom = state[`drawing-${dom_id}`]
        return {
            ...state,
            [`drawing-${dom_id}`]: {
                ...curr_dom,
                active_color
            }
        }
    },
    [types.ERROR](state, { payload }) {
        return {
            ...state
        }
    },
    [types.TYPE_SELECTED](state, { enabled, drawing_type, brush_tool_open, dom_id }) {
        const curr_dom = state[`drawing-${dom_id}`]
        return {
            ...state,
            [`drawing-${dom_id}`]: {
                ...curr_dom,
                drawing_type,
                enabled,
                brush_tool_open
            }
        }
    },
    [types.IMAGE_CONVERTED](state, { blob, dom_id }) {
        const curr_dom = state[`drawing-${dom_id}`]
        return {
            ...state,
            [`drawing-${dom_id}`]: {
                ...curr_dom,
                image: blob
            }
        }
    }
})
