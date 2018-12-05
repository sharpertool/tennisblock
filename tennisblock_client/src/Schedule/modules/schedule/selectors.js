export const blockUpdates = ({ blockUpdates }) => ({ ...blockUpdates })

export const getBlockPlayers = ({ blockplayers }) => (blockplayers)

export const getCouples = ({ blockplayers }) => ({couples: [...blockplayers.couples] })

export const getSubs = ({ subs }) => ({subs: [...subs.guysubs, ...subs.galsubs] })

export const isBlockPlayerEdited = ({ blockplayers, originalCouples }) => {
  const couples = Object.assign({}, blockplayers.couples)
  const base = Object.assign({}, originalCouples)
  return JSON.stringify(base) !== JSON.stringify(couples)
}

export const getGuySubOptions = ({ subs, originalCouples }) => {
  const { guysubs } = subs
  return Object.keys(originalCouples).reduce((result, key) => {
    const guyPlayers = guysubs && guysubs.concat([originalCouples[key].guy])
    result[key] = guyPlayers && guyPlayers.map((player) => {
      return {
        label: player.name,
        value: player.id,
        key: Number(key),
        gender: 'guy',
        player
      }
    })
    return result
  }, {})
}

export const getGalSubOptions = ({ subs, originalCouples }) => {
  const { galsubs } = subs
  return Object.keys(originalCouples).reduce((result, key) => {
    const galPlayers = galsubs && galsubs.concat([originalCouples[key].gal])
    result[key] = galPlayers && galPlayers.map((player) => {
      return {
        label: player.name,
        value: player.id,
        key: Number(key),
        gender: 'gal',
        player
      }
    })
    return result
  }, {})
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
