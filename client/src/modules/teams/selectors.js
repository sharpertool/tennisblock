
export const playSchedule = state => state.schedule
export const validPlaySchedule = state => { return state.schedule != []}
export const calcResult = state => state.schedule_result

export const get_iterations = state => state.iterations
export const get_tries = state => state.tries
export const get_fpartner = state => state.fpartner
export const get_fteam = state => state.fteam
export const get_low_threshold = state => state.low_threshold
