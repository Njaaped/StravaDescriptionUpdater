import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { API_BASE_URL } from '../Config';

function StravaCallback() {
    const location = useLocation();
    const navigate = useNavigate();

    useEffect(() => {
        const searchParams = new URLSearchParams(location.search);
        const code = searchParams.get('code');

        if (code) {
            console.log("Authorization code:", code);
            handleCode(code);
        }
    }, [location]);


    const handleCode = async (code) => {
        
        console.log("Authorization code:", code);
        console.log("Username:", localStorage.getItem('username'));

        const response = await fetch(`${API_BASE_URL}/api/userwithcode`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: localStorage.getItem('username'), code: code })
        });

        const data = await response.json();
        if (data.status === 'success') {
            localStorage.setItem('authorized', 'true');
            navigate('/'); 
            console.log('Should have navigated:', data.message);
        } else {
            console.error('Failed to authorize user:', data.message);
        }
    };

    return (
        <div>
            <h1>Authorization Successful</h1>
        </div>
    );
}

export default StravaCallback;