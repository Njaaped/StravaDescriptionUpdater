
import sqlite3
import requests
from gettokens import get_access_token
import re
import math
import os
from dotenv import load_dotenv
import random
from powercalculation import PowerCalculator

# Load environment variables from .env file
load_dotenv()


keywords = {
    'activity': [
        'average_watts', 'weighted_average_watts', 'max_watts',
        'average_speed', 'max_speed', 'average_cadence',
        'average_temp', 'calories', 'moving_time',
        'elapsed_time', 'total_elevation_gain', 'distance',
        'power'
    ],
    'user': [
        'ytd_ride_count', 'ytd_ride_distance', 'ytd_ride_moving_time',
        'ytd_ride_elevation_gain', 'all_ride_count', 'all_ride_distance',
        'all_ride_moving_time', 'all_ride_elevation_gain', 'ytd_run_count',
        'ytd_run_distance', 'ytd_run_moving_time', 'ytd_run_elevation_gain',
        'all_run_count', 'all_run_distance', 'all_run_moving_time', 'all_run_elevation_gain'
    ]
}

DATABASE_FILE = os.getenv('DATABASE_FILE')
STRAVA_API_URL = os.getenv('STRAVA_API_URL')


def get_activity_keyword_data(data, keywords):
    """Converts keywords to data for activity."""
    activity_data = {}
    for keyword in keywords:
        new_keyword = keyword.split('_')
        try:
            if new_keyword[-1] == 'time':
                activity_data[keyword] = convert_seconds_to_hours(data[keyword])
            elif new_keyword[-1] == 'distance':
                activity_data[keyword] = f'{data[keyword] // 1000}'
            elif new_keyword[-1] == 'speed':
                activity_data[keyword] = f"{convert_mps_to_kmph(data[keyword]):.2f}"
            elif new_keyword[-1] == 'temp':
                activity_data[keyword] = f"{data[keyword]}°C"
            else:
                activity_data[keyword] = data[keyword]
        except:
            activity_data[keyword] = "N/A"
  
    return activity_data

def get_user_keyword_data(data, keywords):
    """Converts keywords to data for user"""

    user_data = {}

    for keyword in keywords:
        new_keyword = keyword.split('_')
        middleword = "_".join(new_keyword[:2]) + "_totals"
        try:
            if new_keyword[-1] == 'time':
                user_data[keyword] = convert_seconds_to_hours(data[middleword]['_'.join(new_keyword[2:])])
            elif new_keyword[-1] == 'distance':
                user_data[keyword] = f"{math.floor(data[middleword]['_'.join(new_keyword[2:])] // 1000)}"
            else:
                user_data[keyword] = data[middleword]['_'.join(new_keyword[2:])]
        except:
            user_data[keyword] = "N/A"
       
    return user_data

def convert_mps_to_kmph(mps):
    return mps * 3.6

def convert_seconds_to_hours(seconds):
    hours = math.floor(seconds // 3600)
    minutes = math.floor((seconds % 3600) // 60)
    return f'{hours}h {minutes}m'

def query_db(query, args=()):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query, args)
        return cursor.fetchone()

def fetch_from_db(query, args=()):
    result = query_db(query, args)
    return result[0] if result else None

def get_username_from_strava_user_id(strava_user_id):
    result = query_db("SELECT DISTINCT username FROM usernameStravaId WHERE id = ? LIMIT 1", (strava_user_id,))
    return result[0] if result else None

def get_refresh_token(username):
    return fetch_from_db("SELECT DISTINCT refreshToken FROM userRefreshToken WHERE username = ? LIMIT 1", (username,))

def get_description_from_username(username, activity_type):
    return fetch_from_db("SELECT description FROM description WHERE username = ? AND type = ? LIMIT 1", (username, activity_type))

def replace_keywords(description, user_data, activity_data) -> str:
    """Replaces keywords in a description with corresponding data."""
    for key in user_data:
        description = description.replace(f'{{{key}}}', str(user_data[key]))
    for key in activity_data:
        description = description.replace(f'{{{key}}}', str(activity_data[key]))
    return description

def get_keywords(description) -> tuple:
    keywords_in_description = re.findall(r'\{(.*?)\}', description)
    new_user_keywords = []
    new_activity_keywords = []
    for keyword in keywords_in_description:
        if keyword in keywords['user']:
            new_user_keywords.append(keyword)
        elif keyword in keywords['activity']:
            new_activity_keywords.append(keyword)
        else:
            print(f"keyword: {keyword} not found in user_keywords or activity_keywords")
        
    return new_user_keywords, new_activity_keywords

def get_user_and_activity_data(user_data, data, user_keywords, activity_keywords) -> tuple:
    user_data = get_user_keyword_data(user_data, user_keywords)
    activity_data = get_activity_keyword_data(data, activity_keywords)

    return user_data, activity_data


def handle_activity(activity_id: int, strava_user_id: int) -> dict:
    """Handle the processing of an activity based on its ID and the user's Strava ID."""
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    username = get_username_from_strava_user_id(strava_user_id)
    print("username: ", username)
    refresh_token = get_refresh_token(username)
    access_token = get_access_token(refresh_token, client_id, client_secret)

    activity_data = get_activity_data(activity_id, access_token)
    if activity_data['type'] in ['VirtualRide', 'Ride']:
        description = get_description_from_username(username,'Ride')
        if strava_user_id == os.getenv('OWNERID'):
            if description == None:
                description = ""
            description = get_ride_outdoor(description, access_token, activity_id)
    elif activity_data['type'] in ['Run']:
        description = get_description_from_username(username,'Run')
    else:
        description = ""

    handle_all(activity_data, access_token, description)

def handle_all(data, access_token, description) -> dict:
    print("handling...", description)
    athlete_id = data['athlete']['id']
    user_data_from_api = make_api_request(
        url=f"{STRAVA_API_URL}/athletes/{athlete_id}/stats",
        headers={'Authorization': f"Bearer {access_token}"}
    )

    new_user_keywords, new_activity_keywords = get_keywords(description)

    user_data, activity_data = get_user_and_activity_data(user_data_from_api, data, new_user_keywords, new_activity_keywords)

    description = replace_keywords(description, user_data, activity_data)

    change_description(access_token, data['id'], description)

    return user_data_from_api

def make_api_request(url, headers, params=None, method='GET'):
    """Makes an API request to the specified URL."""
    response = requests.request(method, url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def get_activity_data(activity_id, access_token):
    """Fetches activity data from Strava."""
    return make_api_request(
        url=f"{STRAVA_API_URL}/activities/{activity_id}",
        headers={'Authorization': f"Bearer {access_token}"}
    )

def change_description(access_token, activity_id, new_description):
    """Updates the description of an activity on Strava."""
    return make_api_request(
        url=f"{STRAVA_API_URL}/activities/{activity_id}",
        headers={'Authorization': f"Bearer {access_token}"},
        params={'description': new_description},
        method='PUT'
    )

    

def get_ride_outdoor(description, access_token, activity_id):
    """Creates custom description for rides with watts data"""
    response = make_api_request(
        url=f"{STRAVA_API_URL}/activities/{activity_id}/streams",
        headers={'Authorization': f"Bearer {access_token}"},
        params={'keys': 'watts,time', 'key_by_type': 'true'}
    )

    try:
        watts = response['watts']['data']
        time = response['time']['data']
    except:
        print("No watts data found.")
        return description

    watts = [150 if x == None else x for x in watts]
    power_calculator = PowerCalculator(watts, time)
    new_description = ""
    wanted = {"1s" : 1, "1m" : 60, "5m" : 300, "10m" : 600, "20m" : 1200, "1h" : 3600}
    emojis = ["⚡️", "🚀", "🧨", "💣", "💨", "✈️", "🛩️", "🦅", "🐎", "🐆","🦍", "💥", "🔥", "🚵🏼", "🚴🏼‍♂️", "🚅", "🚄"]
    for key, val in wanted.items():
        try:
            pwn = round(power_calculator.get_max_power(val))
        except:
            pwn = "N/A"
        new_description += f"{key} -> {pwn}W {random.choice(emojis)}\n"
    new_description += f"Normalized Power: {power_calculator.calculate_normalized_power():.2f}W ⚡️\n"
    print(new_description, description)
    return new_description + description
    

