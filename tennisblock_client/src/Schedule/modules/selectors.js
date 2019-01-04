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

import {globalizeSelectors} from '~/utils'

import {
  selectors as ssel,
  MODULE_NAME as schedule_name,
  set_global_selectors as sset
} from './schedule'
import {
  selectors as tsel,
  MODULE_NAME as team_name,
  set_global_selectors as test
} from './teams'

// Spread out globalized selectors into a single globalized selector structure
// Note that any name conflicts will use the last named selector in the list.
const selectors = {
  ...globalizeSelectors(ssel, schedule_name),
  ...globalizeSelectors(tsel, team_name),
}

sset(selectors)
test(selectors)

export { selectors }
