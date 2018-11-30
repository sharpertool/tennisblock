import React from 'react'
import { FormGroup } from 'reactstrap'
import PropTypes from 'prop-types'
import Select from 'react-select'

const selectBox = (props) => {
  return (
    <FormGroup>
      <Select defaultValue={props.defaultValue} options={props.options} />
    </FormGroup>
  )
}

selectBox.propTypes = {
  defaultValue: PropTypes.number.isRequired,
  onChange: PropTypes.func.isRequired,
  options: PropTypes.arrayOf(PropTypes.object),
  label: PropTypes.string.isRequired,
  isActive: PropTypes.bool,
}


export default selectBox