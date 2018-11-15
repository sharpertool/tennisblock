import axios from 'axios'

const instance = axios.create({
  // ToDo: need a solution that works for deployed app.
  baseURL: `${window.location.protocol}//${window.location.host}`
})

export default instance
