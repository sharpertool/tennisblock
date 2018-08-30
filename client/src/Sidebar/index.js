import React from 'react'
import '~/static/index.scss'
import { render as react_render } from 'react-dom'
import SidebarProvider from './provider'
import map from 'lodash/map'
export default class {
    constructor(target) {
        this.sidebar = document.querySelector(target)
    }
    render({ hierarchy_data, settings }) {

        const style = document.createElement('style')

        const screens = {
            mobile: '576px',
            tablet: '768px',
            desktop: '992px'
        }

        style.innerHTML = map(settings, (v, k) =>
            `@media only screen and (min-width: ${screens[k]}) {
                body {
                    --screen-content-height: ${v};
                }
            }`
        ).toString().replace(/,/g, '').trim()

        document.head.append(style)

        if(hierarchy_data) {
            react_render(<SidebarProvider data={hierarchy_data} />, this.sidebar)
            return
        }
        console.error('no supplied data')
    }
}
