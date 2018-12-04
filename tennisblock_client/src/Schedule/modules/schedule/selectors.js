export const blockUpdates = state => ({ ...state.blockUpdates })

export const getBlockPlayers = ({ schedule }) => (schedule.blockplayers)

export const getCouples = ({ schedule }) => ({couples: [...schedule.blockplayers.couples] })

export const getSubs = ({ schedule }) => ({subs: [...schedule.subs.guysubs, ...schedule.subs.galsubs] })
