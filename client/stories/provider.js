import React from 'react'
import { Provider } from 'react-redux'

const makeProvider = (store) => {
  return (props) => {
    const {story} = props
    return (
    <Provider store={store}>
      {story}
    </Provider>
    )
  }
}

export default makeProvider
