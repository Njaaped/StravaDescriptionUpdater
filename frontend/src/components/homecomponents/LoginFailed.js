import React from 'react';

function LoginFailed({ onRetry }) {
    return (
        <div className='failedDiv'>
            <p>Login Failed</p>
            <button onClick={onRetry} className='failedButton'>
                Try Again
            </button>
        </div>
    );
}

export default LoginFailed;