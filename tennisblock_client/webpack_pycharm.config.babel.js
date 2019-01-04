export default () => {
  console.log(`Build NODE_ENV: ${JSON.stringify(process.env.NODE_ENV)}`)
  //console.log(`Build Stage: ${JSON.stringify(process.env)}`)
  //console.log(`Build Version: ${JSON.stringify(process.env.BUILD_VERSION)}`)
  
  const env = {stage: 'dev'}
  const options = {}
  
  return require(`./config/${env.stage}.js`).default({env, options})
}
