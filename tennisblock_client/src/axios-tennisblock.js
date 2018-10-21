import axios from 'axios'

const instance = axios.create({
  // ToDo: need a solution that works for deployed app.
  baseURL: 'https://tennisblock.local:8002'
})

export default instance

