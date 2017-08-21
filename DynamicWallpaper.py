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
API_KEY = "69672045099f49c86d7d612f0a6ce9b2"

MOMENTS = {"DAY": 1, "NIGHT": 1, "MORNING": 3, "AFTERNOON": 2, "EVENING":3}


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
        return None
    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    return [sunrise, sunset]

def get_time_moment():
    """
    Get the time moment of the day.
    """
    return choose_moment(get_available_moment())

def get_available_moment():
    """
    Compute and return the moment of the day.
    """
    actual_time = datetime.datetime.now()

    return ["NOPE"]

def choose_moment(moment_list):
    """
    Randomize moment.
    """
    return moment_list[0]

def __main__():
    options = set_os_attribute()
    moment = get_time_moment()
    exit(0)
