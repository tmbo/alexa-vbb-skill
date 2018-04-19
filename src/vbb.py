import json
import logging
import math
from datetime import datetime

import requests
from builtins import str

from src import config
from src import utils

PRODUCTS = ["S-Bahn", "U-Bahn", "Tram", "Bus", "", "ICE/IC", "RE/RB"]

ALL_PRODUCTS = math.pow(2, len(PRODUCTS)) - 1


def vbb_api(method, **kwargs):
    if kwargs:
        params = "&" + "&".join([k + "=" + str(v) for k, v in kwargs.items()])
    else:
        params = ""
    r = requests.get(config.vbb_base_url + "/{}?format=json&"
                                           "accessId={}{}"
                                           "".format(method, config.vbb_token,
                                                     params))
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        logging.error("Failed to request {}. Status: {} Error: "
                      "".format(method, r.status_code, r.text))
        return {}


def fetch_stops_by_name(name):
    r = vbb_api("location.name", input=name)
    return r.get("stopLocationOrCoordLocation", [])


def fetch_next_trains_for_stop(station_id=config.default_station_id,
                               products=1,
                               min_wait=2,
                               max_wait=120):
    r = vbb_api("departureBoard", products=products, id=station_id,
                maxJourneys=20)
    departures = r.get("Departure", [])
    return next_stop_per_direction(departures, min_wait, max_wait)


def vbb_time_to_datetime(time, date):
    try:
        return datetime.strptime(time + " " + date, '%H:%M:%S %Y-%m-%d')
    except Exception:
        logging.error("Failed to parse datetime. "
                      "date: '{}' time: {}".format(date, time))
        return None


def simplify_direction(direction_name):
    replacements = {"S+U ": "", "S ": "", "U ": "", " (Berlin)": "",
                    " Bhf": ""}
    for s, r in replacements.items():
        direction_name = direction_name.replace(s, r)
    return direction_name.strip()


def direction_id(train_result):
    name = train_result.get("name", "").strip()
    return name, simplify_direction(train_result.get("direction"))


def next_stop_per_direction(next_trains, min_wait, max_wait):
    next_per_destination = {}
    for t in next_trains:
        tid = direction_id(t)
        time = vbb_time_to_datetime(t.get("rtTime", t.get("time")),
                                    t.get("rtDate", t.get("date")))
        if time and (tid not in next_per_destination or (
                tid in next_per_destination and
                next_per_destination[tid]["time"] > time)):
            m = utils.wait_time_in_minutes(time)
            if min_wait <= m < max_wait:
                next_per_destination[tid] = {
                    "time": time,
                    "name": t.get("name", "").strip(),
                    "direction": simplify_direction(t.get("direction"))
                }

    next_stops = []
    while next_per_destination:
        ns = sorted(next_per_destination.keys(),
                    key=lambda e: next_per_destination.get(e)["time"])[:2]
        for n in ns:
            next_stops.append(next_per_destination[n])
        for n in ns:
            for k in next_per_destination.keys():
                if k[0] == n[0]:
                    del next_per_destination[k]

    return next_stops


def station_in_direction(direction):
    results = vbb_api("location.name", input=direction, products=115,
                      type="S", maxNo=100)
    if not results:
        return None
    exact_matches = []
    for result in results.get("stopLocationOrCoordLocation", []):
        if direction in result.get("StopLocation", {}).get("name", ""):
            exact_matches.append(result["StopLocation"])

    if not exact_matches:
        exact_matches.extend(results[:1])
    r = sorted(exact_matches, key=lambda e: -e.get("weight", 0))
    return r[0]


if __name__ == '__main__':
    print(station_in_direction("Berlin"))
