export const blockUpdates = ({ blockUpdates }) => ({ ...blockUpdates })

export const getBlockPlayers = ({ blockplayers }) => (blockplayers)

export const getCouples = ({ blockplayers }) => ({couples: [...blockplayers.couples] })

export const getSubs = ({ subs }) => ({subs: [...subs.guysubs, ...subs.galsubs] })

export const getGuySubs = ({ subs_guys }) => (subs_guys)

export const getGalSubs = ({ subs_gals }) => (subs_gals)

export const isBlockPlayerEdited = ({ blockplayers, originalCouples }) => {
  const couples = Object.assign({}, blockplayers.couples)
  const base = Object.assign({}, originalCouples)
  return JSON.stringify(base) !== JSON.stringify(couples)
}

export const changes = ({ originalCouples, blockplayers }) => {
  const { couples } = blockplayers
  return Object.keys(originalCouples).reduce((result, key) => {
    result[key] = {
      guy: originalCouples[key].guy.id !== couples[key].guy.id,
      gal: originalCouples[key].gal.id !== couples[key].gal.id
    }
    return result
  }, {})
}
