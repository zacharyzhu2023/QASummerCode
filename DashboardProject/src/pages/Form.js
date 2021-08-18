import { useState } from 'react'
import './Form.css';
import FormField from '../components/FormField'
import FormDropdown from '../components/FormDropdown'
import { API, Auth} from 'aws-amplify';
import {withAuthenticator } from '@aws-amplify/ui-react';

// The Form that the tester uses to enter in a new test result
const Form = () => {
    const [firstName, setFirstname] = useState('')
    const [lastName, setLastName] = useState('')
    const [batchNumber, setBatchNumber] = useState('')
    const [serialNumber, setSerialNumber] = useState('')
    const [comment, setComment] = useState('')
    const [isSuccess, setIsSuccess] = useState(true)

    const [serialNumberGet, setSerialNumberGet] = useState('')

    // Dropdown failure options
    const failureOptions = [
        { value: 'connectionError', label: 'No Wifi Connection' },
        { value: 'borkenError', label: 'Camera Broken' },
        { value: 'error', label: 'Error' },
        { value: 'failureError', label: 'Failure' }
      ]

    async function formAPICall(e){
        // Prevents the form from refreshing until the API call is complete
        e.preventDefault()

        // API call
        const user = await Auth.currentAuthenticatedUser()
        const token = user.signInUserSession.idToken.jwtToken
        console.log({ token })

        // Get the current Date
        let newDate = new Date();
        let year = newDate.getFullYear();
        let month = newDate.getMonth()+1;
        let date = newDate.getDate();
        
        // Format data for input into database
        let fullDate = year + "-" + month + "-" + date;
        let fullName = firstName + " " + lastName

        const requestInfo = {
            headers: {
                Authorization: token
                },
            body: {
                "function": "insertEntry",
                "sn": serialNumber,
                "bn": batchNumber,
                "date": fullDate,
                "tst": fullName,
                "ft": isSuccess,
                "fail": "None",
                "msg": comment
              }
        }
        const data = await API.post('dashboardProjectAPI','/dashboardFormat', requestInfo)
        console.log({ data })
        
        // Rest the form
        setFirstname('')
        setLastName('')
        setBatchNumber('')
        setSerialNumber('')
        setComment('')
        setIsSuccess(true)
    }

    async function getAPICall(e){
        // Prevents the form from refreshing until the API call is complete
        e.preventDefault()

        // API call
        const user = await Auth.currentAuthenticatedUser()
        const token = user.signInUserSession.idToken.jwtToken
        console.log({ token })

        const requestInfo = {
            headers: {
                Authorization: token
            },
            body: {
                "function": "getEntry",
                "sn": serialNumberGet,
              }
        }
        const data = await API.get('dashboardProjectAPI','/dashboardFormat', requestInfo)
        console.log({ data })
        
        // Rest the field
        setSerialNumberGet('')
    }

    async function deleteAPICall(e){
        // Prevents the form from refreshing until the API call is complete
        e.preventDefault()

        // API call
        const user = await Auth.currentAuthenticatedUser()
        const token = user.signInUserSession.idToken.jwtToken
        console.log({ token })

        const requestInfo = {
            headers: {
                Authorization: token
            },
            body: {
                "function": "deleteEntry",
                "sn": serialNumberGet,
              }
        }
        const data = await API.del('dashboardProjectAPI','/dashboardFormat', requestInfo)
        console.log({ data })
        
        // Rest the field
        setSerialNumberGet('')
    }
      
  return (
      <div>
      <form className='form' onSubmit={formAPICall}>
        <div className='flex'>
            <FormField fieldTitle="First Name" fieldPlaceholder="John" fieldText={firstName} setText={setFirstname}/>
            <FormField fieldTitle="Last Name" fieldPlaceholder="Doe" fieldText={lastName} setText={setLastName}/>
        </div>
        <FormField fieldTitle="Batch Number" fieldPlaceholder="23" fieldText={batchNumber} setText={setBatchNumber}/>
        <FormField fieldTitle="Serial Number" fieldPlaceholder="G8B1900000VD3" fieldText={serialNumber} setText={setSerialNumber}/>

        <hr className="topBreaker" />
        {/* <FormCheckbox checkboxTitle="Success"/>
        <FormCheckbox checkboxTitle="Fail" /> */}
        <div className='form-control form-control-check'>
            <label>Success</label>
            <input type='radio' checked={isSuccess} value={isSuccess} onChange={(e) => setIsSuccess(e.currentTarget.checked)}/>
        </div>
        <div className='form-control form-control-check'>
            <label>Failure</label>
            <input type='radio' checked={!isSuccess} value={!isSuccess} onChange={(e) => setIsSuccess(!e.currentTarget.checked)}/>
        </div>
        {!isSuccess && <FormDropdown dropdownTitle="Failure Category" dropdownOptions={failureOptions}/>}
        <hr className="bottomBreaker"/>

        <FormField fieldTitle="Comment/Issue" fieldPlaceholder="Jira Ticket: WPT-423" fieldText={comment} setText={setComment}/>

        <input type='submit' value='Submit Test' className='btn btn-block' />
      </form>

      <FormField fieldTitle="Serial Number" fieldPlaceholder="G8B1900000VD3" fieldText={serialNumberGet} setText={setSerialNumberGet}/>
      <button className='btn btn-block' onClick={getAPICall}> Get Data</button>
      <button className='btn btn-block' onClick={deleteAPICall}> Delete Data</button>
      </div>
  )
}

export default Form
