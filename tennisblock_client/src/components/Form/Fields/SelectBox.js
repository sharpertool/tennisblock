import React, { Fragment } from 'react'
import Toggle from '~/hoc/Toggle'
import PropTypes from 'prop-types'

const selectBox = (props) => {
  return (
    <Fragment>
      <div className="select-label" onClick={() => props.onToggle}>{props.label}</div>
      {props.isActive &&
        <div className="select-options">
          {props.options && props.options.map((option, key) => {
                return (
                  <div key={key} className="select-option"
                    onClick={() => props.onChange(option.id)}>
                    { option.name }
                  </div>
                )
              }
            )}
          </div>
      }
    </Fragment>
  )
}

selectBox.propTypes = {
  onToggle: PropTypes.func.isRequired,
  options: PropTypes.arrayOf(PropTypes.object),
  label: PropTypes.string.isRequired,
  isActive: PropTypes.bool,
}


export default selectBox