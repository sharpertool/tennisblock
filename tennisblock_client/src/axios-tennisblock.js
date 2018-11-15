import axios from 'axios'

const instance = axios.create({
  // ToDo: need a solution that works for deployed app.
  baseURL: 'http://tennisblock.local:8000',
})

export default instance
