import { gactions as schedule_actions } from '~/modules/schedule'
import { gactions as teams_actions } from '~/modules/teams'

export const actions = {
    ...schedule_actions,
    ...teams_actions,
}
