

const enable = () => {
  const force = typeof(window.__FORCE_LOGS__) !== 'undefined'
  const is_prod = process.env.NODE_ENV === 'production'
  return force || !is_prod
}

const log = (...args) => {
  if (typeof(console) !== 'undefined' && enable()) {
    console.log(...args)
  }
}

export default log
