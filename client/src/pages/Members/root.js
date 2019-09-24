import React from 'react'
import {Provider} from 'react-redux'


const root = ({store}) => {
  
  return (
    <Provider store={store}>
      <div className={'dynamic'}>
        <h3>Block Members - React</h3>
      </div>
    </Provider>)
}

export default root
