import React from 'react'
import { API, Auth} from 'aws-amplify';
import { withAuthenticator, AmplifySignOut } from '@aws-amplify/ui-react';



function SignIn() {
    return (
        <div className='bold'>
            <AmplifySignOut />
        </div>
    )
}

export default withAuthenticator(SignIn);