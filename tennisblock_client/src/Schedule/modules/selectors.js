/****
 * Globalize the selectors in the modules
 *
 * I'm looking for a more generic way to do this,
 * but basically this takes a list of all exported selectors from
 * a module and globalizes it.
 *
 * Selectors in a module are written to take the state as defined
 * in the module.
 *
 * When we use the selectors at the Component level, the component is
 * going to see the entire state tree, so a 'module' selector must
 * be globalized so that it can get the appropriate state to act on
 *
 * Here I am doing this "per module", which is a little verbose, but
 * until I get a lot of modules.. i am better doing it this way than
 * worrying about it.
 *
 * I added an improved version of this that takes care of additional
 * arguments that a selector might take. It assumes that the state is the
 * first argument, but then spreads any additional arguments onto the
 * composed globalized selector.
 */
import _ from 'lodash'

import {selectors as ssel, NAME as schedule_name} from './schedule'
import {selectors as tsel, NAME as team_name} from './teams'

// This version requires lodash.. not sure if there is an advantage??
const fromRoot = (path) =>
  (selector) =>
    (state, ...args) =>
      selector(_.get(state, path), ...args);

// Version that does not require lodash
const fromRoot2 = (path) =>
  (selector) =>
    (state, ...args) =>
      selector(state[path], ...args);

const globalizeSelectors = (selectors,path) => {
  return Object.keys(selectors).reduce((final, key) => {
    final[key] = fromRoot2(path)(selectors[key]);
    return final;
  }, {});
};

// Spread out globalized selectors into a single globalized selector structure
// Note that any name conflicts will use the last named selector in the list.
const selectors = {
  ...globalizeSelectors(ssel, schedule_name),
  ...globalizeSelectors(tsel, team_name),
}

export { selectors }
