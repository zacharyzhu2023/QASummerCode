import { useState } from 'react'
import '../pages/Form.css';


const FormField = ({ fieldTitle, fieldPlaceholder, fieldText, setText }) => {

  return (
    <div className='form-field'>
        <div className='form-control'>
        <label>{fieldTitle}</label>
        <input
            type='text'
            placeholder={fieldPlaceholder}
            value={fieldText}
            onChange={(e) => setText(e.target.value)}
        />
        </div>
    </div>
  )
}


export default FormField
