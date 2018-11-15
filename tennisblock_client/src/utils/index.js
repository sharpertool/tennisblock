import { APP_NAME } from '~/constants'

export function studlyCase(string) {
  return string.replace(/[\-|\_]/g, ' ')
  .replace(/\w\S*/g, str => {
      return str.charAt(0).toUpperCase() + str.substr(1).toLowerCase();
  })
  .replace(/\s/g, '')
  .replace(/\w\S*/g, str => {
      return str.charAt(0).toLowerCase() + str.substr(1);
  });
}
// Sample createConstrants that I've create
export const createConstants = (parent = null, name) => (...actionTypes) => {
  return actionTypes.reduce((acc, type) => {
  
    const typesWithPrefixes = [parent && parent, name, type].filter(Boolean).join('/')
    
    acc[type.toUpperCase()] = studlyCase(typesWithPrefixes)
    
    return acc
  
  }, {})
}


export const actionType = (type, moduleName) => [APP_NAME, moduleName, name].join('/').toLowerCase()