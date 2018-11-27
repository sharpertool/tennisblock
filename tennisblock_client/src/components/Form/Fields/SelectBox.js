import React from 'react'
import { FormGroup, Label, Input } from 'reactstrap'
import PropTypes from 'prop-types'

const selectBox = (props) => (
  <FormGroup>
    <Input type="select" name="select"
      onChange={(e) => { 
        props.onChange(props.defaultValue, e.target.value)
      }} defaultValue={props.defaultValue}>
      <option value={props.id}>{props.label}</option>
      {props.options && props.options.map((option, index) => (
        <option key={index} value={option.id}>{option.name}</option>
      ))}
    </Input>
  </FormGroup>
)

selectBox.propTypes = {
  defaultValue: PropTypes.number.isRequired,
  onChange: PropTypes.func.isRequired,
  options: PropTypes.arrayOf(PropTypes.object),
  label: PropTypes.string.isRequired,
  isActive: PropTypes.bool,
}


export default selectBox