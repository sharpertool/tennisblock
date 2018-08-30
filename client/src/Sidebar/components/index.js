import jump from 'jump.js'
import { hot } from 'react-hot-loader'
import React, { Component } from 'react'
import {Treebeard} from 'react-treebeard'
import Sidebar from './Sidebar'
import { types } from '~/Sidebar/modules/Scroll'
import ContentContainer, { Content } from './Content'

class SidebarTree extends Component {
    state = {
        cursor: {
            active: false
        }
    }
    handleToggle(node, toggled) {
        const { dispatch } = this.props
        if(this.state.cursor){
            console.log(this.state.cursor)
            this.state.cursor.active = false
        }

        node.active = true

        if(node.children) {
            node.toggled = toggled
        }

        const { slug } = node

        const target = document.getElementById(slug)

        const navbar_height = document.getElementById('header').offsetHeight

        if(target) {
            jump(target, {
                offset: -navbar_height
            })
        } else {
            dispatch({ type: types.GET_DIRECT_CONTENT, slug })
        }


        this.setState({ cursor: node })
    }
    render() {
        const { handleToggle, props } = this
        const { data, Scroll: { prepending, appending } } = props

        return[
            <Sidebar key={0} {...props} />,
            <ContentContainer key={1}>
                {prepending ?
                        <div className="col-12 text-center">
                            Loading...
                        </div> : null}
                <Content {...props} />
                {appending ?
                    <div className="col-12 text-center">
                        Loading...
                    </div> : null}
            </ContentContainer>
        ]
    }
}

export default SidebarTree
