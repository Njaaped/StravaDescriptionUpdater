import React from "react";
import { STRAVA_CLIENT_ID, STRAVA_REDIRECT_URI } from '../../Config';

function StravaAuthLink() {
    const clientId = `${STRAVA_CLIENT_ID}`;
    const redirectUri = encodeURIComponent("https://njalstravaapp.onrender.com/callback");
    const scope = encodeURIComponent("activity:read_all,activity:write");

    const authUrl = `https://www.strava.com/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=${scope}`;
    return (
        <a href={authUrl}>Connect with Strava</a>
    );
}

export default StravaAuthLink;