import { bool, func } from 'prop-types'

const propTypes = {
  isOpen: bool.isRequired,
  toggle: func.isRequired,
  onConfirm: func.isRequired
}

export default propTypes
