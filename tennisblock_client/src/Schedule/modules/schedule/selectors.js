export const blockUpdates = ({ blockUpdates }) => ({ ...blockUpdates })

export const getBlockPlayers = ({ blockplayers }) => (blockplayers)

export const getCouples = ({ blockplayers }) => ({couples: [...blockplayers.couples] })

export const getSubs = ({ subs }) => ({subs: [...subs.guysubs, ...subs.galsubs] })

export const isBlockPlayerEdited = ({ blockplayers, originalCouples }) => {
  const couples = Object.assign({}, blockplayers.couples)
  const base = Object.assign({}, originalCouples)
  return JSON.stringify(base) !== JSON.stringify(couples)
}

export const getGuySubOptions = ({ subs, blockplayers }) => {
  const { couples } = blockplayers
  const { guysubs } = subs

  return (couples || []).reduce((result, value, index) => {
    const guyPlayers = guysubs && [couples[index].guy].concat(guysubs)
    result[index] = guyPlayers && guyPlayers.map((player) => {
      return {
        label: player.name,
        value: player.id,
        key: Number(index),
        gender: 'guy',
        player
      }
    })
    return result
  }, [])
}

export const getGalSubOptions = ({ subs, blockplayers }) => {
  const { couples } = blockplayers
  const { galsubs } = subs

  return (couples || []).reduce((result, value, index) => {
    const galPlayers = galsubs && [couples[index].gal].concat(galsubs)
    result[index] = galPlayers && galPlayers.map((player) => {
      return {
        label: player.name,
        value: player.id,
        key: Number(index),
        gender: 'gal',
        player
      }
    })
    return result
  }, [])
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
