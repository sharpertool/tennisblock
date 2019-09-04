import * as config  from './config'

export default (env={stage:'dev'}, options) => {
  console.log(`Building stage ${env.stage}`)
  console.log(`Build NODE_ENV: ${JSON.stringify(process.env.NODE_ENV)}`)

  if (env.stage in config) {
    return config[env.stage]({env, options})
  }

  console.log(`env.stage must be one of ${Object.keys(config).join('.')}`)
  return () => {}
}
