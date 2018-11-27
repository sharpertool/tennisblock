export const blockUpdates = state => ({ ...state.blockUpdates })

export const getCouples = ({ schedule }) => ({couples: [...schedule.blockplayers.couples] })

export const getSubs = ({ schedule }) => ({subs: [...schedule.subs.guysubs, ...schedule.subs.galsubs] })