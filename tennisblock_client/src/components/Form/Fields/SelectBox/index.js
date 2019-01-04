import React from 'react'
import { FormGroup } from 'reactstrap'
import PropTypes from 'prop-types'
import Select from 'react-select'
import styles from './styles.local.scss'

const selectBox = (props) => {
  return (
    <FormGroup>
      <Select
        defaultValue={props.defaultValue}
        options={props.options}
        onChange={props.onChange}
        className={props.isChanged ? styles.Changed : ''}/>
    </FormGroup>
  )
}

selectBox.propTypes = {
  defaultValue: PropTypes.object.isRequired,
  onChange: PropTypes.func.isRequired,
  options: PropTypes.arrayOf(PropTypes.object),
  label: PropTypes.string,
  isActive: PropTypes.bool,
  isChanged: PropTypes.bool
}


export default selectBox
