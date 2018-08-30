import { combineReducers } from 'redux'
import { createRootReducer as processModules } from 'redux-module-builder'

import * as Drawing from '~/ImageEditor/modules/Drawing'
import * as Modal from '~/ImageEditor/modules/Modal'
/**
 * You can register your modules here
 * @type {Object}
 */
const modules = {
    Drawing,
    Modal
}

const initialActions = {
}

/**
 * You can add reducers from external npm modules
 * @type {Object}
 */
const initialReducers = {}

const initialState = {}

/**
 * We are actually processing the modules why call createRootReducer if the function generates actions
 * @type {object}
 */
const bundled = processModules(modules, {
    initialInitialState: initialState,
    initialActions,
    initialReducers
})

const reducers = combineReducers(bundled.reducers)

/**
 * Function to activate the generated bundle
 * @return {object} reducers, actions, inititalState
 */
export default () => {
    return {
        reducers,
        actions: bundled.actions,
        initialState: bundled.initialState
    }
}
