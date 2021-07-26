import argparse
import requests
import time
import threading
import random

# GLOBAL
test_mode = False


class SetFrequency(threading.Thread):
    def __init__(self, func, freq: int):
        '''calls the @func function after @freq seconds
        :param func: function to call
        :param freq: time in seconds between each call of the @func function
        '''
        self.func = func
        self.freq = freq

        super().__init__()
        self.setDaemon(True)

    def run(self) -> None:
        start_time = time.time()
        while 1:
            self.func()
            # accurate way to calculate time to wait
            time.sleep(self.freq - (time.time() - start_time) % self.freq)


def monitor_datadog_status() -> None:
    """
    this function prints DataDog's non-operational components statuss.
    """
    # defining helper function to process respond
    def process_datadog_status(data: dict) -> None:
        """
        helper function to process/filter the json respond from the API,
        and print the non-operational components.
        :param data: the json respond from the API.
        """
        # this is only used for testing mode (* for now)
        statuses = set("operational", "partial_outage",
                       "major_outage", "degraded_performance", "maintenance")

        for component in data["components"]:
            if test_mode:
                print("TESTING MODE IS ON - THIS IS NOT THE REAL STATUS!")
                component["status"] = random.choice(statuses)
            if "operational" not in component["status"]:
                now = time.strftime("%d/%m/%Y %H:%M:%S")
                print(
                    f'{now} Component {component["name"]} is in status: {component["status"]}')

    # The API's URL
    URL = "https://status.datadoghq.com/api/v2/components.json"
    res = requests.get(URL)
    if res.status_code == 200:
        process_datadog_status(res.json())
    else:
        print("Faild to get API respond...")


if __name__ == '__main__':
    # creating parser for CLI and it's arguments
    parser = argparse.ArgumentParser(
        description="checks DataDog's component status at a regular frequency.")
    # frequency argument
    parser.add_argument('-f', '--frequency', required=True, type=float,
                        help="Enter the frequency at which you want to check DataDog's component status.")
    # testing argument - flase by default
    parser.add_argument('--test', action='store_false')

    args = parser.parse_args()

    # if in testing mode
    test_mode = args.test

    # Using a non-blocking way to monitor on a regular frequency
    status_checker = SetFrequency(
        monitor_datadog_status, args.frequency)
    status_checker.start()
    status_checker.join()
