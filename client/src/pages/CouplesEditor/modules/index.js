
/**
These files are autogenerated using gardenbuzz_client/scripts/make_modules.py
DO NOT EDIT THESE FILES!

Re-generate them from the command line:

cd gardenbuzz_client
python ./scripts/make_modules.py src/pages/<page name>/modules_used.json

That will re-build the ./modules directory in the page specified.

*/


import {set_connect_data, redux_connect_data} from '~/redux-page'

import {actions} from './actions'
import {selectors} from './selectors'
import {rootReducer} from './reducer'
import {rootSaga} from './sagas'
import {eventsMap} from './eventsMap'
import {set_config, initialize} from './config'
export {
  actions, 
  selectors, 
  eventsMap, 
  rootReducer, 
  rootSaga, 
  set_config, 
  initialize,
  redux_connect_data,
}

set_connect_data({selectors: selectors, actions: actions})

        