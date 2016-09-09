import requests
import json
from datetime import datetime
from pytz import timezone
from pprint import pprint
from config import sunsetLatitude, sunsetLongitude
from memoize import MWT

url = "http://api.sunrise-sunset.org/json?lat="+sunsetLatitude+"&lng="+sunsetLongitude+"&date=today"


@MWT(timeout=60*60)  # timeout = 1 hour
def getTimeOfSunset():  # returns time of sunset in the form of "11:33:27 PM"
    # hit up the API to get the time
    get = requests.get(url)
    apiResp = json.loads(get.text)  # parse the JSON
    # return the time of sunset in the city
    return apiResp["results"]["civil_twilight_end"]


def isSunset():
    time = getTimeOfSunset()  # get the time of the sunset
    (sunset_hours, sunset_minutes, sunset_seconds) = tuple(
        time.replace(' PM', '').split(":"))
    (sunset_hours, sunset_minutes, sunset_seconds) = int(sunset_hours), int(
        sunset_minutes), int(sunset_seconds)  # make them all ints
    currentTime = datetime.now().replace(tzinfo=timezone('UTC'))
    (current_hours, current_minutes) = (currentTime.hour,
                                        currentTime.minute)
    show_time = sunset_minutes - 10 < current_minutes < sunset_minutes
    is_evening = 'PM' in time
    same_hours = sunset_hours == current_hours
    is_wednesday = currentTime.isoweekday() == 3
    return show_time and is_evening and same_hours and is_wednesday


def print_obj_info(obj):  # prints out information about the given object (helper function - never used)
    print('- ' * 10)
    pprint([{item: getattr(obj, item)} for item in dir(obj)])
    print('- ' * 10)
