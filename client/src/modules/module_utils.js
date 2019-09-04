import unapply from 'ramda/src/unapply'
import mergeDeepRight from 'ramda/src/mergeDeepRight'
import reduce from 'ramda/src/reduce'

export const mergeDeepRightAll = unapply(reduce(mergeDeepRight, {}))

export const globalizeActions = (actions, path) => {
  return Object.keys(actions).reduce((final, key) => {
    final[key] = actions[key]
    final[`${path}:${key}`] = actions[key]
    return final
  }, {})
}

