import App from '~/Sidebar/container'
import { Provider } from 'react-redux'
import React, { Component } from 'react'
import composeStore from '~/Sidebar/store'
import SidebarTree from '~/Sidebar/components'
import { types } from '~/Sidebar/modules/Scroll'

export const { store, actions, history } = composeStore(
    null,
    window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__
)

class ClientProvider extends Component {
    componentDidMount() {

        const { data } = this.props
        store.dispatch({ type: types.INITIALIZE,  sidebar_data: data })
    }
    render() {
        return(
            <Provider store={store}>
                <App {...this.props}>
                    <SidebarTree />
                </App>
            </Provider>
        )
    }
}

export default ClientProvider
