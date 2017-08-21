#!/usr/bin/env python3
"""
AWallpaper module
"""
import sys
import ctypes
import os
import datetime
import urllib.request
import json

WIN_DRIVE = "C:\\"
WIN_FOLDER = "Utilisateurs\\quent\\Images\\DynamicWallpaper"
UNI_FOLDER = ""
LOCATION = "Beijing"
LOCATION_GMT = 6
API_KEY = "69672045099f49c86d7d612f0a6ce9b2"

MOMENTS = {"DAY": 1, "NIGHT": 1, "SUNSET": 3, "MORNING": 2, "AFTERNOON": 2, "SUNRISE":3}


def set_os_attribute():
    """
    Initialize OS specific structure.
    """
    res = []
    if sys.platform == "linux" or sys.platform == "linux2":
        # LINUX
        res.append("linux")
        res.append(UNI_FOLDER)
    elif sys.platform == "darwin":
        print("MAC not supported yet.", file=sys.stderr)
        exit(1)
    elif sys.platform == "win32":
        #WINDOWS
        res.append("windows")
        res.append(os.path.join(WIN_DRIVE, WIN_FOLDER))
    else:
        print("Unknown OS.", file=sys.stderr)
        exit(1)
    return res

def get_previous_sunrise_sunset():
    """
    Use openweathermap API to know the sunrise and sunset time
    """
    api_service = "api.openweathermap.org/data/2.5/weather?q="
    request = urllib.request.urlopen(api_service + LOCATION + "&APPID=" + API_KEY).read()
    data = json.load(request)
    if data is None or data["cod"] == "404":
        print("Problem occur during sunrise/sunset data acquisition. \
        Your location may haven't been found. \
        Please check your location or your internet connection.", file=sys.stderr)
        exit(1)
        return None
    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"] + 3600 * LOCATION_GMT)
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"] + 3600 * LOCATION_GMT)
    return [sunrise.hour * 60 + sunrise.minute, sunset.hour * 60 + sunset.minute]

def get_time_moment():
    """
    Get the time moment of the day.
    """
    return choose_moment(get_available_moment())

def get_available_moment():
    """
    Compute and return the moment of the day.
    """
    res = []
    actual_time = datetime.datetime.now()
    actual_time_in_min = actual_time.hour * 60 + actual_time.minute
    sun_data_in_min = get_previous_sunrise_sunset()
    if actual_time_in_min <= sun_data_in_min[0] + 60 and actual_time_in_min >= sun_data_in_min[1] - 60:
        res.append("SUNRISE")
    elif actual_time_in_min <= sun_data_in_min[1] + 60 and actual_time_in_min >= sun_data_in_min[1] - 60:
        res.append("SUNSET")
    if actual_time_in_min <= 12 * 60 and actual_time_in_min > sun_data_in_min[0]:
        res.append("MORNING")
    elif actual_time_in_min >= 12 * 60 and actual_time_in_min < sun_data_in_min[1]:
        res.append("AFTERNOON")
    if actual_time_in_min < sun_data_in_min[0] or actual_time_in_min > sun_data_in_min[1]:
        res.append("NIGHT")
    else:
        res.append("DAY")
    return res

def choose_moment(moment_list):
    """
    Randomize moment.
    """
    return moment_list[0]

def __main__():
    options = set_os_attribute()
    moment = get_time_moment()
    exit(0)
