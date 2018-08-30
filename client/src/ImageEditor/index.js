import 'd3-selection-multi'
import '~/static/index.scss'
import { render } from 'react-dom'
import React, { Component } from 'react'
import ClientProvider from './provider/Client'


export default (target) => {
    const elems = document.querySelectorAll(target)

    if(elems) {
        return elems.forEach((elem, dom_id) => {
            if(elem) {
                if(elem.dataset.values || elem.dataset.props) {
                    const props = {
                        dom_id,
                        image: elem.dataset.props
                    }
                    for(var i in elem.dataset) {

                        props[i] = elem.dataset[i]

                        delete elem.dataset[i]
                    }

                    render(<ClientProvider {...props} />, elem)

                }
            }

        })
    }

    console.error('no dataset')

    return false
}
