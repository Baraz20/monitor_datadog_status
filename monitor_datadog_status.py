import argparse
import requests
import time
from threading import Thread, Timer

def monitor_datadog_status(freq: int) -> None:
    # The API URL
    URL = "https://status.datadoghq.com/api/v2/components.json"
    starttime = time.time()
    while 1:
        proccess_datadog_status(requests.get(URL).json())
        time.sleep(freq - (time.time() - starttime) % freq)

def proccess_datadog_status(data: dict) -> None:
    for component in data["components"]:
        # checks if the status is diffrent from "operational"
        if "operational" not in component["status"]:
            # getting the time and date
            now = time.strftime("%d/%m/%Y %H:%M:%S")
            # printing out to STDIN
            print(
                f'{now} Component {component["name"]} is in status: {component["status"]}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="checks DataDog's componanet status at a regular frequency.")

    parser.add_argument('--frequency', required=True, type=int,
                        help="Enter the frequency at which you want to DataDog's componanet status.")

    args = parser.parse_args()
    freq = args.frequency
    monitor_datadog_status(args.frequency)
