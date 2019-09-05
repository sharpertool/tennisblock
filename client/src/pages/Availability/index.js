import React from 'react';
import {render} from 'react-dom';

import Widget from './Widget'

export default (elements, options) => {
  const {availability_el} = elements
  console.log(`Rendering to target ${availability_el}`)
  render(
    <Widget/>, document.getElementById(availability_el)
  )
}
