/**
 * page.js
 *
 * Place global redux connect data here so that lower-level components can access it.
 *
 */

export let redux_connect_data = {
  selectors: {},
  actions: {},
}

export let selectors  = {}
export let actions = {}

export const set_connect_data = (config) => {
  redux_connect_data = config
  selectors = config.selectors
  actions = config.actions
}

