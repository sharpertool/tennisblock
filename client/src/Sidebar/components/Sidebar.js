import jump from 'jump.js'
import map from 'lodash/map'
import React, { Component } from 'react'
import { types } from '~/Sidebar/modules/Scroll'
import filter from 'lodash/filter'
import conforms from 'lodash/conforms'
import reduce from 'lodash/reduce'

class SidebarSiblings extends Component {
    handleScroll(slug, e) {
        const target = document.getElementById(slug)
        const navbar_height = document.getElementById('header').offsetHeight
        const bookmark_top = document.getElementById('bookmark_top')
        const { dispatch } = this.props
        e.preventDefault()
        if(target) {
            jump(target, {
                offset: -navbar_height
            })
        } else {
            jump(bookmark_top)
            dispatch({ type: types.GET_DIRECT_CONTENT, slug })
        }
    }
    render() {
        const { list, collapsed, active_content } = this.props
        return(
            <ul className={!collapsed ? 'd-none' : ''}>
                {map(list, (v, k) => (
                    <li key={k}>
                        <a className={`list-group-item ${v.slug == active_content ? 'active' : null}`}
                            href="javascript:void(0)" onClick={this.handleScroll.bind(this, v.slug)}>{v.name}</a>
                    </li>
                )) }
            </ul>
        )
    }
}

class SidebarChildren extends Component {
    state = {
        child_collapsed: false
    }
    handleCollapse(slug, e) {
        const target = document.getElementById(slug)
        const navbar_height = document.getElementById('header').offsetHeight
        const { dispatch } = this.props
        e.preventDefault()
        this.setState({ child_collapsed: !this.state.child_collapsed }, () => {
            if(target) {
                jump(target, {
                    offset: -navbar_height
                })
            } else {
                jump(bookmark_top)
                dispatch({ type: types.GET_DIRECT_CONTENT, slug })
            }
        })
    }
    render() {
        const { handleCollapse, state, props } = this
        const { child_collapsed } = state
        const { list, collapsed, active_content, deep_children } = props

        const deep_child_active = (() => {
            return filter(deep_children, conforms({ 'slug': (n) => n == active_content })).length > 0
        })()


        return(
            <ul className={collapsed    ? '' : 'd-none'}>
                {map(list, (v, k) => {
                    const children_active = filter(v.children, (cv, ck) => {

                    })
                    return(<li key={k}>
                        <a className={`list-group-item ${v.slug == active_content ? 'active' : null}`}
                            href="javascript:void(0)"
                            onClick={handleCollapse.bind(this, v.slug)}>{v.name}
                            {v.children ? <i className={`float-right fa fa-chevron-${child_collapsed || active_content == v.slug || deep_child_active ? 'down' : 'right'}`} aria-hidden="true"></i> : null }</a>
                        { v.children ?
                            <SidebarSiblings
                                list={v.children}
                                collapsed={child_collapsed || active_content == v.slug || deep_child_active }
                                active_content={active_content} /> : null }
                    </li>)
                }) }
            </ul>
        )
    }
}

class SidebarParent extends Component {
    state = {
        collapsed: false
    }
    handleCollapse(slug, e) {
        const target = document.getElementById(slug)
        const navbar_height = document.getElementById('header').offsetHeight
        const { dispatch } = this.props
        e.preventDefault()
        this.setState({ collapsed: !this.state.collapsed }, () => {
            if(target) {
                jump(target, {
                    offset: -navbar_height
                })
            } else {
                jump(bookmark_top)
                dispatch({ type: types.GET_DIRECT_CONTENT, slug })
            }
        })
    }
    render() {
        const { handleCollapse } = this
        const { collapsed } = this.state
        const { values, dispatch, active_content, deep_children } = this.props

        const has_active_child = (() => {
            let main_result = []

            if(values.children) {
                main_result = filter(values.children,
                    conforms({ 'slug' : (n) => n == active_content })
                )
                if(main_result.length > 0) {
                    return true
                }

                return false
            }

        })()

        const deep_child_active = (() => {
            return filter(deep_children, conforms({ 'slug': (n) => n == active_content })).length > 0
        })()
        return(
            <li className={values.slug == active_content ? 'active' : null}>
                <a className={`list-group-item ${values.slug == active_content ? 'active' : null}`}
                    href="javascript:void(0)"
                    onClick={handleCollapse.bind(this, values.slug)}>
                    {values.name}
                    {values.children ?
                        <i
                            className={`float-right fa fa-chevron-${collapsed || active_content == values.slug || has_active_child || deep_child_active ? 'down' : 'right'}`}
                            aria-hidden="true"></i> : null }
                </a>
                { values.children ?
                    <SidebarChildren
                        list={values.children}
                        dispatch={dispatch}
                        deep_children={deep_children}
                        active_content={active_content}
                        collapsed={collapsed || active_content == values.slug || has_active_child || deep_child_active } /> : null }
            </li>
        )
    }
}

class SidebarContainer extends Component {
    render() {
        const { data, dispatch, Scroll: { active_content } } = this.props

        const get_children = reduce(data, (r, v, k) => {
            if(v.children) {
                reduce(v.children, (_r, _v, _k) => {
                    r.push(_v)
                }, [])
            }
            return r
        }, [])


        const get_next_child = reduce(get_children, (r, v, k) => {
            if(v.children) {
                reduce(v.children, (_r, _v, _k) => {
                    r.push(_v)
                    return _r
                }, [])
            }
            return r
        }, [])


        return(
            <ul className="jump-menu list-group">
                <li className="input-group">
                    <span className="addon">
                    <i className="fa fa-search"></i>
                    </span>

                    <input type="text" className="form-control" placeholder="Find in Document" />
                </li>
                {map(data, (v, k) => (
                    <SidebarParent key={k} deep_children={get_next_child} dispatch={dispatch} values={v} active_content={active_content} />
                ))}
            </ul>
        )
    }
}


export default SidebarContainer
