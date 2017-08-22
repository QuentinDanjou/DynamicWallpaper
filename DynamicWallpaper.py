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
import random
import glob

WIN_DRIVE = "C:\\"
WIN_FOLDER = "Users\\quent\\Pictures\\DynamicWallpaper"
UNI_FOLDER = ""
LOCATION = "Beijing"
LOCATION_GMT = 8
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
    api_service = "http://api.openweathermap.org/data/2.5/weather?q="
    request = urllib.request.Request(api_service + LOCATION + "&APPID=" + API_KEY)
    print("REQUEST DONE!")
    response = urllib.request.urlopen(request)
    encoding = response.info().get_content_charset('utf8')
    data = json.loads(response.read().decode(encoding))
    if data is None or data["cod"] == "404":
        print("Problem occur during sunrise/sunset data acquisition. \
        Your location may haven't been found. \
        Please check your location or your internet connection.", file=sys.stderr)
        exit(1)
        return None
    print(data["sys"]["sunrise"])
    print(data["sys"]["sunset"])
    sunrise = datetime.datetime.utcfromtimestamp(data["sys"]["sunrise"])
    sunset = datetime.datetime.utcfromtimestamp(data["sys"]["sunset"])
    print("sunrise: " + str(sunrise.hour) + ":" + str(sunrise.minute))
    print("sunset: " + str(sunset.hour) + ":" + str(sunset.minute))
    sunrise_conv = (sunrise.hour * 60 + sunrise.minute + 60 * LOCATION_GMT) % 1440
    sunset_conv = (sunset.hour * 60 + sunset.minute + 60 * LOCATION_GMT) % 1440
    return [sunrise_conv, sunset_conv]

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
    print("Previous sunrise, sunset:")
    print(sun_data_in_min)
    if actual_time_in_min <= sun_data_in_min[0] + 60 \
    and actual_time_in_min >= sun_data_in_min[1] - 60:
        res.append("SUNRISE")
    elif actual_time_in_min <= sun_data_in_min[1] + 60\
    and actual_time_in_min >= sun_data_in_min[1] - 60:
        res.append("SUNSET")
    if actual_time_in_min <= 12 * 60 and actual_time_in_min > sun_data_in_min[0]:
        res.append("MORNING")
    elif actual_time_in_min >= 12 * 60 and actual_time_in_min < sun_data_in_min[1]:
        res.append("AFTERNOON")
    if actual_time_in_min < sun_data_in_min[0] or actual_time_in_min > sun_data_in_min[1]:
        res.append("NIGHT")
    else:
        res.append("DAY")
    print(res)
    return res

def choose_moment(moment_list):
    """
    Randomize moment.
    """
    randomizer = []
    for moment in moment_list:
        randomizer.extend([moment for i in range(MOMENTS[moment])])
    return randomizer[random.randint(0, len(randomizer) - 1)]

def set_wallpaper(sys_options, moment):
    print(os.path.join(sys_options[1], moment, "*"))
    all_paths = glob.glob(os.path.join(sys_options[1], moment, "*"))
    # No file checking for the moment.
    print(all_paths)
    if not all_paths:
        return False
    choosen_imgpath = all_paths[random.randint(0, len(all_paths) - 1)]
    if sys_options[0] == "windows":
        print(choosen_imgpath)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, choosen_imgpath, 3)
        print("wallpaper is set.")

    return True

if __name__ == "__main__":
    print("STARTING")
    succeed = False
    SYS_OPTIONS = set_os_attribute()
    print("OPTIONS DONE")
    print(SYS_OPTIONS)
    loop_protection = 0
    while succeed is False:
        loop_protection += 1
        result_moment = get_time_moment()
        print(result_moment)
        succeed = set_wallpaper(SYS_OPTIONS, result_moment)
        if loop_protection > 20:
            print("Can't find a wallpaper.", file=sys.stderr)
            exit(1)
    exit(0)
