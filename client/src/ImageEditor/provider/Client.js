import React, { Component } from 'react'
import { Provider } from 'react-redux'
import composeStore from '~/ImageEditor/store'


import App from '~/ImageEditor/containers/App'
import Drawing from '~/ImageEditor/components/Drawing'
import ImageControls from '~/ImageEditor/components/ImageControls'

import { types } from '~/ImageEditor/modules/Drawing'


export const { store, actions, history } = composeStore(
    null,
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
)

class ClientProvider extends Component {
    componentDidMount() {
        const { dom_id, image } = this.props
        store.dispatch({ type: types.INITIALIZE, dom_id, image })
    }
    render() {
        const { dom_id } = this.props
        return(
            <Provider store={store}>
                <App {...this.props}>
                    <Drawing
                        actions={actions}
                        width="100%"
                        height="100%" />
                    <ImageControls />
                </App>
            </Provider>
        )
    }
}

export default ClientProvider
