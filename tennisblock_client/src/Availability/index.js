import React from 'react';
import {render} from 'react-dom';

import Widget from '~/Availability/Widget'

export default (target) => {
  if (target) {
    render(
      <Widget/>, target
    )
  }

  return false;
}
