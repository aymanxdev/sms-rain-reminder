import requests
from twilio.rest import Client
import os


endpoint_base = 'https://api.openweathermap.org/data/2.5/onecall'
account_sid = os.environ.get('AUCC_SID') #twilio ACCOUNT_SID
auth_token = os.environ.get('AUTH_TOKEN') #twilio Authentication Token
api_key = os.environ.get('API_KEY') #Open Weather Map API_KEY
weather_params = {
    "lat": 51.501720,
    "lon": -0.097960,
    "appid": api_key,
    "exclude": 'current,daily,minutely'
}

response = requests.get(endpoint_base, params=weather_params)
response.raise_for_status()
print(response.status_code)
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

raining = False
for hourly_data in weather_slice:
    weather_code = hourly_data["weather"][0]["id"]
    if int(weather_code) < 700:
        raining = True

if raining:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body="It's going to rain today, bring an umbrella ☂",
        from_='From number from Twilio account',
        to='your phone number'
    )

    print(message.status)
