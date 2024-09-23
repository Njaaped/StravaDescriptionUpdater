import React, { useState } from 'react';
import './DescriptionDisplay.css'; // Importing the CSS file for styling
import { API_BASE_URL } from '../../Config';


function DescriptionDisplay() {
    const [description, setDescription] = useState('');
    const [activityType, setActivityType] = useState('Run'); // Default to 'Run'
    const [showKeywords, setShowKeywords] = useState(false); // State to toggle keywords display

    const activityKeywords = [
        'average_watts', 'weighted_average_watts', 'max_watts', 'average_speed', 'max_speed',
        'average_cadence', 'average_temp', 'calories', 'moving_time', 'elapsed_time',
        'total_elevation_gain', 'distance'
    ];

    const userKeywords = [
        'ytd_ride_count', 'ytd_ride_distance', 'ytd_ride_moving_time', 'ytd_ride_elevation_gain',
        'all_ride_count', 'all_ride_distance', 'all_ride_moving_time', 'all_ride_elevation_gain',
        'ytd_run_count', 'ytd_run_distance', 'ytd_run_moving_time', 'ytd_run_elevation_gain',
        'all_run_count', 'all_run_distance', 'all_run_moving_time', 'all_run_elevation_gain'
    ];

    const handleInputChange = (event) => {
        setDescription(event.target.value);
    };

    const handleTypeChange = (event) => {
        setActivityType(event.target.value);
    };

    const handleSubmit = async (event) => {
        event.preventDefault(); // Prevent the default form submit behavior
        try {
            const response = await fetch(`${API_BASE_URL}/api/receive_description`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    description: description,
                    username: localStorage.getItem('username'),
                    type: activityType // Include the activity type in the POST request
                })
            });
            const data = await response.json();
            console.log('Response from server:', data);
            alert('Description submitted successfully!');
        } catch (error) {
            console.error('Failed to submit description:', error);
            alert('Failed to submit description.');
        }
    };

    const toggleKeywords = () => {
        setShowKeywords(!showKeywords);
    };

    return (
        <div className="description-container">
            <h1>Write Your Preference Description</h1>
            <button onClick={toggleKeywords} className="keywords-toggle">
                {showKeywords ? 'Hide Keywords' : 'Show Keywords'}
            </button>
            {showKeywords && (
                <div className="keywords-list">
                    <h2>Activity Keywords:</h2>
                    <ul>{activityKeywords.map(keyword => <li key={keyword}>{keyword}</li>)}</ul>
                    <h2>User Keywords:</h2>
                    <ul>{userKeywords.map(keyword => <li key={keyword}>{keyword}</li>)}</ul>
                </div>
            )}
            <form onSubmit={handleSubmit} className="description-form">
                <textarea
                    value={description}
                    onChange={handleInputChange}
                    className="description-textarea"
                    placeholder="Enter your description here..."
                />
                <div className="type-selector">
                    <label>
                        <input
                            type="radio"
                            value="Run"
                            checked={activityType === 'Run'}
                            onChange={handleTypeChange}
                        />
                        Run
                    </label>
                    <label>
                        <input
                            type="radio"
                            value="Ride"
                            checked={activityType === 'Ride'}
                            onChange={handleTypeChange}
                        />
                        Ride
                    </label>
                </div>
                <button type="submit" className="submit-button">Submit</button>
            </form>
        </div>
    );
}

export default DescriptionDisplay;