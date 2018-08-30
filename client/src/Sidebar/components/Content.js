import React, { Component } from 'react'
import { createPortal } from 'react-dom'
import { types } from '~/Sidebar/modules/Scroll'
import map from 'lodash/map'
import last from 'lodash/last'
import first from 'lodash/first'

const mount = document.getElementById('content-container')

const TOP_GAP = 1000

export class Content extends Component {

    componentDidMount() {
        document.addEventListener('scroll', this.scrollObserver.bind(this))
    }

    scrollObserver() {
        const yCoordinate = window.scrollY + TOP_GAP

        const contents  = this.refs.contents.childNodes

        const content_top = this.refs.contents.offsetTop
        const content_bottom = this.refs.contents.offsetHeight


        const { dispatch } = this.props

        const array_contents = [...contents]

        const active_content = this.getActiveContent(array_contents)

        this.setActiveLink(active_content)

        const last_child = last(array_contents)
        //ajax request and validate first child or last child of children_content



        if(yCoordinate >= content_bottom) {
            if(last_child) {
                dispatch({
                    type: types.GET_NEXT_CONTENT,
                    last_child: last_child.id
                })
            }
        } else if(window.scrollY <= content_top) {
            if(first(array_contents)) {
                const first_child = first(array_contents).id
                dispatch({ type: types.GET_PREV_CONTENT, first_child })
            }
        }


    }

    setActiveLink(active_content) {
        const { dispatch } = this.props

        dispatch({ type: types.SET_ACTIVE_CONTENT, active_content })

    }

    getActiveContent(contents) {
        const yCoordinate = window.scrollY
        const sidebar_top = document.querySelector('.datapages-sidebar').offsetTop
        const content = contents.filter((d, key) => {
            return d.offsetTop >= sidebar_top
        })[0]

        if(content) {
            return content.id
        }
    }

    render() {
        const { props } = this

        const { Scroll: { contents } } = props
        //https://reactjs.org/docs/dom-elements.html#dangerouslysetinnerhtml
        return(
            <div
                ref="contents"
                className="contents col-12"
                dangerouslySetInnerHTML={{
                    __html: contents.toString().replace(/,/g, '')
                }} />
        )

    }
}

class ContentContainer extends Component {
    render() {
        return createPortal(this.props.children, mount)
    }
}


export default ContentContainer
