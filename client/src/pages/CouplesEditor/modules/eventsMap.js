
/**
These files are autogenerated using gardenbuzz_client/scripts/make_modules.py
DO NOT EDIT THESE FILES!

Re-generate them from the command line:

cd gardenbuzz_client
python ./scripts/make_modules.py src/pages/<page name>/modules_used.json

That will re-build the ./modules directory in the page specified.

*/

import {mergeDeepRightAll} from '~/modules/module_utils'

import { eventsMap as season_map } from '~/modules/season'

export const eventsMap = mergeDeepRightAll(season_map)
export default eventsMap

