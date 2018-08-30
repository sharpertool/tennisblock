export default (env, options) => {
    console.log(`Build NODE_ENV: ${JSON.stringify(process.env.NODE_ENV)}`)
    //console.log(`Build Stage: ${JSON.stringify(process.env)}`)
    //console.log(`Build Version: ${JSON.stringify(process.env.BUILD_VERSION)}`)

    return require(`./config/${env.stage}.js`).default({ env, options })
}
