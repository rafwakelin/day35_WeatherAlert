import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

API_EPOINT = "http://api.openweathermap.org/data/3.0/onecall"

api_key = # YOUR OPEN WEATHER MAP API KEY
account_sid = # YOUR TWILIO ACCOUNT SID
auth_token = # YOUR TWILIO ACCOUNT PHONE NUMBER

loc_latitude = 25.204849
loc_longitude = 55.270782


parameters = {"lat": loc_latitude,
              "lon": loc_longitude,
              "appid": api_key,
              "exclude": "current,minutely,daily",
              }

api_response = requests.get(url=API_EPOINT, params=parameters)
api_response.raise_for_status()
data = api_response.json()
weather_data = data["hourly"][:12]

rainy_day = False

for hourly_data in weather_data:
    weather_code = hourly_data["weather"][0]["id"]
    if int(weather_code) < 700:
        rainy_day = True

if rainy_day:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages \
        .create(
            body="It will rain today. Drive carefully 🚘 and buy an umbrella ☔️.",
            from_="+17269007220",
            to=# YOUR PHONE NUMBER
            )
    print(message.status)
