import React from 'react';
import StravaAuthLink from './StravaAuthLink';

function CredentialsDisplay({ username, message }) {
    return (
        <div className="credentials-display">
            <p className='successmessage'>{message}</p>
            <h1>Welcome, {username}!</h1>
            <StravaAuthLink />
        </div>
    );
}

export default CredentialsDisplay;