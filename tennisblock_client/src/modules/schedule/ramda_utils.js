import * as R from 'ramda'

export const groupByGenderAndId = R.reduceBy(
  (acc, {id}) => acc.concat(id),
  [],
  ({gender}) => gender == 'f' ? 'curr_gals' : 'curr_guys'
)
export const toObjectById = R.chain(R.zipObj, R.pluck('id'))


