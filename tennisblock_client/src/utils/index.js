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

// Version that does not require lodash
const fromRoot2 = (path) =>
  (selector) =>
    (state, ...args) =>
      selector(state[path], ...args);

export const globalizeSelectors = (selectors,path) => {
  return Object.keys(selectors).reduce((final, key) => {
    final[key] = fromRoot2(path)(selectors[key]);
    return final;
  }, {});
};


export const actionType = (type, moduleName) => [APP_NAME, moduleName, type].join('/').toLowerCase()

export const LocalDate = (date) => {
  const [yy, mm, dd] = date.split('-')
  return new Date(yy, mm-1, dd)
}