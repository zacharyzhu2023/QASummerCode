import { useState } from 'react'
import '../pages/Form.css';
import Select from 'react-select';

// A dropdown component
const FormDropdown = ({ dropdownTitle, dropdownOptions }) => {
  const options = dropdownOptions

  return (
      <div className='form-dropdown'>
          <label>{dropdownTitle}</label>
          <Select options={options} />
      </div>
    
  )
}

export default FormDropdown
