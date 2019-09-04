import {moduleConfig as config} from './config';

export const validateFile = (file) => {
  let result = {
    is_valid: true,
    message: '',
    file: ''
  }
  
  const size_limit = config['file_size_limit']
  const size_limit_text = config['file_size_limit_text']
  
  if (file && file.length > 0) {
    const selected_file = file[0]
    // validate file size, should be less than specified limit
    if (selected_file.size > size_limit) {
      result['message'] = `File should be less than ${size_limit_text}`
      result['is_valid'] = false
    }
    
    const type = selected_file.type
    if (type !== 'image/png' && type !== 'image/jpeg') {
      // validate file type, should be JPG or PNG
      result['message'] = 'File type should be JPG or PNG'
      result['is_valid'] = false
    }
    
    result['file'] = selected_file
  } else {
    result['is_valid'] = false
  }
  
  return result
}

