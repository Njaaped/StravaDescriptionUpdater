import React from 'react';

function StartScreen({ handleLoginClick }) {
    return (
        <>
            <p> Want to have your own automatic description? </p>
            <button className="get-started-button" onClick={handleLoginClick}>Get Started</button>
        </>
    );
}

export default StartScreen;