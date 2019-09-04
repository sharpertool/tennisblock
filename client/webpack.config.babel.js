export default (env = {stage: 'dev'}, options) => {
  console.log(`Build NODE_ENV: ${JSON.stringify(process.env.NODE_ENV)}`)
  //console.log(`Build Stage: ${JSON.stringify(process.env)}`)
  //console.log(`Build Version: ${JSON.stringify(process.env.BUILD_VERSION)}`)
  console.log(env)
  if (env === 'undefined') {
    env = {stage: 'dev'}
  }
  
  return require(`./config/${env.stage}.js`).default({env, options})
}
