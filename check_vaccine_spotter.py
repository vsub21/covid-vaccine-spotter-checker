import os
import requests
import json

from time import time, localtime, sleep, strftime
from datetime import datetime
import sched

import winsound

USPS_STATE_ABB = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
}

BEEP_DURATION = 1000 # milliseconds
BEEP_FREQ = 440 # Hz

def check_cvs(os_type, abb):
    found_any = False

    url = f"https://www.vaccinespotter.org/api/v0/states/{abb}.json"
    json = requests.get(url).json()

    features = json["features"]
    for f in features:
        p = f["properties"]
        if p["appointments_available"]:
            if not found_any:
                found_any = True
            
            print(f"\n===== APPOINTMENT FOUND ! ===== ")
            
            provider_brand_name = p["provider_brand_name"]
            name = p["name"]
            full_address = f"{p['address']}\n{p['city']}, {p['state']} {p['postal_code']}"
            appt_url = f"{p['url']}"

            lf = p["appointments_last_fetched"]
            dot_pos = lf.find('.')
            plus_pos = lf.find('+')
            lf = (lf[:dot_pos] + lf[plus_pos:])
            last_fetched = f"Last fetched from source: {datetime.fromisoformat(lf).astimezone().strftime('%m/%d/%Y, %H:%M:%S')}"

            print(provider_brand_name)
            print(name)
            print(full_address)
            print(last_fetched)
            print(appt_url)
            
    if found_any:
        for _ in range(3):
            if os_type == "0": # Windows
                winsound.Beep(BEEP_FREQ, BEEP_DURATION)
            else: # Mac/Linux
                os.system(f"play -nq -t alsa synth {BEEP_DURATION} sine {BEEP_FREQ}")
    else:
        print("No appointments found.\n")

        lf = json["metadata"]["appointments_last_fetched"]
        dot_pos = lf.find('.')
        plus_pos = lf.find('+')
        lf = (lf[:dot_pos] + lf[plus_pos:])
        last_fetched = f"Last fetched from source: {datetime.fromisoformat(lf).astimezone().strftime('%m/%d/%Y, %H:%M:%S')}"

        print(last_fetched)

def daemon(local_handler, t, os_type, abb, freq):
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"COVID-19 Vaccine Spotter last checked: {strftime('%m/%d/%Y, %H:%M:%S', localtime())}")
    check_cvs(os_type, abb)
    local_handler.enterabs(t + freq, 1, daemon, (local_handler, t + freq, os_type, abb, freq))

def main():
    os_type = input("Enter '0' for Windows, '1' for Linux/Mac: ")
    while os_type != "0" and os_type != "1":
        os_type = input("Invalid entry. Enter '0' for Windows, '1' for Linux/Mac: ")
    if os_type == "0":
        import winsound

    abb = input("Enter the 2-letter abbreviation for your U.S. state: ").upper()
    while abb not in USPS_STATE_ABB.keys():
        abb = input("Invalid entry. Enter the 2-letter abbreviation for your U.S. state: ")
    state = USPS_STATE_ABB[abb]
    print(f"Checking for vaccines in state: {state}")

    freq = input("Enter frequency of checking website (in whole number of seconds). Leave blank for default 30 seconds: ")
    if not freq:
        freq = "30"
    while not freq.isdigit():
        freq = input("Invalid entry. Enter frequency of checking website (in whole number of seconds). Leave blank for default 30 seconds: ")
    freq = int(freq)

    handler = sched.scheduler(time, sleep)
    t = time()
    handler.enter(0, 1, daemon, (handler, t, os_type, abb, freq))
    handler.run()

if __name__ == "__main__":
    main()
