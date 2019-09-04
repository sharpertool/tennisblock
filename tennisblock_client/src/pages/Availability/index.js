import React from 'react';
import {render} from 'react-dom';

import Widget from './Widget'

export default (target) => {
  if (target) {
    render(
      <Widget/>, target
    )
  }

  return false;
}
